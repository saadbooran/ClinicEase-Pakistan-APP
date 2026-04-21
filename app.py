import os
import io
import json
import re
import base64
import tempfile

from flask import Flask, request, jsonify, send_file, render_template
from dotenv import load_dotenv
from openai import OpenAI

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# ---------------- CONFIG ---------------- #

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

# ---------------- GROQ CLIENT ---------------- #

groq_client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# ---------------- UTIL ---------------- #

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def image_to_base64(image_bytes, filename):
    ext = filename.rsplit('.', 1)[-1].lower()
    mime_map = {'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'png': 'image/png', 'webp': 'image/webp'}
    mime = mime_map.get(ext, 'image/jpeg')
    b64 = base64.b64encode(image_bytes).decode('utf-8')
    return b64, mime


# ---------------- VISION LLM PARSER ---------------- #

def parse_prescription_with_vision(image_bytes, filename):
    b64, mime = image_to_base64(image_bytes, filename)

    prompt = """You are a medical prescription extraction AI with vision capability.

Look at this prescription image carefully and extract ALL visible information.

The prescription may be:
- Handwritten or printed
- In English, Urdu, Hindi, Kannada, or mixed languages
- From any country (Pakistan, India, etc.)
- Containing abbreviations like: C/o, Dx, Rx, OD, BD, TDS, QID, SOS, IV, IM, SC, stat, PRN
- Containing vital signs: BP, PR, RR, Temp, RBS, SpO2

Return STRICT JSON only — no explanation, no markdown:

{
  "patient_name": string or null,
  "patient_age": number or null,
  "patient_sex": string or null,
  "doctor_name": string or null,
  "doctor_qualification": string or null,
  "clinic_hospital": string or null,
  "date": string or null,
  "ref_no": string or null,
  "vitals": {
    "bp": string or null,
    "pulse": string or null,
    "temperature": string or null,
    "rbs": string or null,
    "spo2": string or null
  },
  "chief_complaint": string or null,
  "diagnosis": string or null,
  "medicines": [
    {
      "name": string,
      "generic_name": string or null,
      "dosage": string or null,
      "route": string or null,
      "frequency": string or null,
      "duration": string or null,
      "instructions": string or null
    }
  ],
  "general_instructions": [string] or [],
  "follow_up": string or null,
  "diet_advice": string or null,
  "notes": string or null,
  "confidence": "high" | "medium" | "low"
}

Rules:
- Read ALL text in the image carefully, including headers, stamps, and handwriting
- For dosage patterns like 4+4+4 or 1-0-1, note them as morning+afternoon+night
- Set confidence "high" if prescription is clearly readable and complete
- DO NOT hallucinate — only extract what you can actually see
- Return ONLY valid JSON"""

    response = groq_client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime};base64,{b64}"
                        }
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ],
        temperature=0.1,
        max_tokens=1500
    )

    content = response.choices[0].message.content
    # Strip markdown fences if present
    content = re.sub(r'^```(?:json)?\s*', '', content.strip())
    content = re.sub(r'\s*```$', '', content.strip())
    content = content.strip()

    try:
        result = json.loads(content)
        result['ai_provider'] = 'Groq (Llama 4 Scout Vision)'
        return result
    except Exception:
        # Try to salvage partial JSON
        try:
            start = content.index('{')
            end = content.rindex('}') + 1
            result = json.loads(content[start:end])
            result['ai_provider'] = 'Groq (Llama 4 Scout Vision)'
            return result
        except Exception:
            return {
                "error": "JSON parsing failed",
                "raw": content,
                "medicines": [],
                "confidence": "low"
            }


# ---------------- PDF GENERATION ---------------- #

def generate_pdf(data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            leftMargin=40, rightMargin=40,
                            topMargin=40, bottomMargin=40)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('CustomTitle', parent=styles['Title'],
                                 textColor=colors.HexColor('#0d9488'),
                                 fontSize=20, spaceAfter=6)
    heading_style = ParagraphStyle('CustomHeading', parent=styles['Heading2'],
                                   textColor=colors.HexColor('#115e59'),
                                   fontSize=13, spaceBefore=12, spaceAfter=4)
    body_style = ParagraphStyle('CustomBody', parent=styles['Normal'],
                                fontSize=10, spaceAfter=3)

    story = []
    story.append(Paragraph("Rx Reader — Prescription Report", title_style))
    story.append(Spacer(1, 8))

    # Patient / Doctor info
    vitals = data.get('vitals') or {}
    info_fields = [
        ('Patient Name', data.get('patient_name')),
        ('Patient Age', data.get('patient_age')),
        ('Patient Sex', data.get('patient_sex')),
        ('Doctor Name', data.get('doctor_name')),
        ('Qualification', data.get('doctor_qualification')),
        ('Clinic / Hospital', data.get('clinic_hospital')),
        ('Date', data.get('date')),
        ('Ref / UHID No', data.get('ref_no')),
        ('Chief Complaint', data.get('chief_complaint')),
        ('Diagnosis', data.get('diagnosis')),
        ('Blood Pressure', vitals.get('bp')),
        ('Pulse', vitals.get('pulse')),
        ('Temperature', vitals.get('temperature')),
        ('RBS', vitals.get('rbs')),
        ('SpO2', vitals.get('spo2')),
    ]
    info_data = [[k, str(v)] for k, v in info_fields if v]
    if info_data:
        story.append(Paragraph("Patient & Doctor Information", heading_style))
        tbl = Table(info_data, colWidths=[150, 330])
        tbl.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0fdfa')),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#0f766e')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#ccfbf1')),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(tbl)
        story.append(Spacer(1, 8))

    medicines = data.get('medicines', [])
    if medicines:
        story.append(Paragraph("Prescribed Medicines", heading_style))
        med_data = [['#', 'Medicine', 'Dosage/Route', 'Frequency', 'Duration']]
        for i, m in enumerate(medicines, 1):
            dosage = ' '.join(filter(None, [m.get('dosage'), m.get('route')])) or '—'
            med_data.append([
                str(i),
                m.get('name', '—'),
                dosage,
                m.get('frequency') or '—',
                m.get('duration') or '—',
            ])
        tbl = Table(med_data, colWidths=[25, 160, 100, 100, 70])
        tbl.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0d9488')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0fdfa')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#ccfbf1')),
            ('PADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(tbl)
        story.append(Spacer(1, 8))

    for label, key in [("General Instructions", 'general_instructions')]:
        val = data.get(key, [])
        if val:
            story.append(Paragraph(label, heading_style))
            for item in val:
                story.append(Paragraph(f"• {item}", body_style))

    for label, key in [("Follow-up", 'follow_up'), ("Diet Advice", 'diet_advice'), ("Notes", 'notes')]:
        val = data.get(key)
        if val:
            story.append(Paragraph(label, heading_style))
            story.append(Paragraph(str(val), body_style))

    story.append(Spacer(1, 16))
    disclaimer_style = ParagraphStyle('Disclaimer', parent=styles['Normal'],
                                      fontSize=8, textColor=colors.HexColor('#64748b'))
    story.append(Paragraph(
        "Medical Disclaimer: This AI summary is for informational purposes only and does not replace "
        "professional medical advice. Always follow your doctor's original prescription.",
        disclaimer_style
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer


# ---------------- ROUTES ---------------- #

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files.get('prescription')

    if not file or file.filename == '':
        return jsonify({'error': 'No file uploaded'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Allowed: PNG, JPG, JPEG, WEBP'}), 400

    try:
        image_bytes = file.read()
        result = parse_prescription_with_vision(image_bytes, file.filename)

        return jsonify({
            "success": True,
            "data": result
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/download-pdf', methods=['POST'])
def download_pdf():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        pdf_buffer = generate_pdf(data)
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='prescription_summary.pdf'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ---------------- URDU TRANSLATION ---------------- #

@app.route('/translate-urdu', methods=['POST'])
def translate_urdu():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data'}), 400

    summary_lines = []
    if data.get('patient_name'):   summary_lines.append(f"Patient Name: {data['patient_name']}")
    if data.get('patient_age'):    summary_lines.append(f"Age: {data['patient_age']}")
    if data.get('patient_sex'):    summary_lines.append(f"Sex: {data['patient_sex']}")
    if data.get('doctor_name'):    summary_lines.append(f"Doctor: {data['doctor_name']}")
    if data.get('clinic_hospital'):summary_lines.append(f"Hospital: {data['clinic_hospital']}")
    if data.get('date'):           summary_lines.append(f"Date: {data['date']}")
    if data.get('chief_complaint'):summary_lines.append(f"Complaint: {data['chief_complaint']}")
    if data.get('diagnosis'):      summary_lines.append(f"Diagnosis: {data['diagnosis']}")
    vitals = data.get('vitals') or {}
    if vitals.get('bp'):    summary_lines.append(f"Blood Pressure: {vitals['bp']}")
    if vitals.get('pulse'): summary_lines.append(f"Pulse: {vitals['pulse']}")
    if vitals.get('rbs'):   summary_lines.append(f"RBS: {vitals['rbs']}")

    meds = data.get('medicines', [])
    for i, m in enumerate(meds, 1):
        med_str = f"Medicine {i}: {m.get('name','')}"
        if m.get('dosage'):     med_str += f", Dosage: {m['dosage']}"
        if m.get('frequency'):  med_str += f", Frequency: {m['frequency']}"
        if m.get('route'):      med_str += f", Route: {m['route']}"
        if m.get('duration'):   med_str += f", Duration: {m['duration']}"
        if m.get('instructions'): med_str += f", Note: {m['instructions']}"
        summary_lines.append(med_str)

    instructions = data.get('general_instructions', [])
    for inst in instructions:
        summary_lines.append(f"Instruction: {inst}")
    if data.get('follow_up'):   summary_lines.append(f"Follow-up: {data['follow_up']}")
    if data.get('diet_advice'): summary_lines.append(f"Diet: {data['diet_advice']}")

    english_summary = "\n".join(summary_lines)

    prompt = f"""You are a medical translator for Pakistani patients.

Translate the following prescription summary into clear, simple Urdu (Nastaliq script).
Use language that a regular Pakistani patient can easily understand.
Format it nicely with line breaks between sections.
Use these section headers in Urdu: مریض کی معلومات، تشخیص، دوائیں، ہدایات

English Summary:
{english_summary}

Return ONLY the Urdu translation. No English. No explanation."""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a professional Urdu medical translator. Return only Urdu text."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=1000
    )
    urdu_text = response.choices[0].message.content.strip()
    return jsonify({'urdu': urdu_text})


# ---------------- MEDICINE DETAIL ---------------- #

@app.route('/medicine-detail', methods=['POST'])
def medicine_detail():
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'error': 'No medicine name'}), 400

    med_name = data['name']
    generic_name = data.get('generic_name', '')

    prompt = f"""You are a medical information assistant.

Provide detailed information about this medicine and return STRICT JSON only:

Medicine name: {med_name}
Generic name: {generic_name or 'unknown'}

Return this exact JSON structure:
{{
  "category": string (e.g. "Antibiotic", "Analgesic", "IV Fluid", etc.),
  "use": string (what it is used to treat, 2-3 sentences),
  "how_it_works": string (simple explanation of mechanism, 1-2 sentences),
  "side_effects": string (common side effects, comma-separated),
  "precautions": string (important precautions, 2-3 sentences),
  "storage": string (how to store it),
  "image_search_term": string (best Google Images search term to find a photo of this medicine/pill/vial)
}}

Rules:
- Use simple, patient-friendly language
- Be accurate and factual
- Return ONLY valid JSON, no markdown"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Return only valid JSON. No markdown. No explanation."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        max_tokens=700
    )

    content = response.choices[0].message.content
    content = re.sub(r'^```(?:json)?\s*', '', content.strip())
    content = re.sub(r'\s*```$', '', content.strip())

    try:
        detail = json.loads(content)
        # Build a Google image search URL for the medicine
        search_term = detail.get('image_search_term', med_name + ' medicine tablet')
        image_url = f"https://source.unsplash.com/400x200/?medicine,pill,tablet,{search_term.replace(' ',',')}"
        # Use a reliable open image source via Wikipedia/OpenFDA style search term
        # We'll pass back a placeholder that the frontend can use
        return jsonify({
            'detail': detail,
            'image_url': f"https://via.placeholder.com/400x200/0d9488/ffffff?text={med_name.replace(' ','+')}"
        })
    except Exception:
        return jsonify({
            'detail': {
                'use': 'Could not load details. Please consult your pharmacist.',
                'side_effects': None,
                'precautions': None,
                'storage': None,
                'category': None,
                'how_it_works': None
            },
            'image_url': None
        })


# ---------------- RUN ---------------- #

if __name__ == '__main__':
    app.run(debug=True)
