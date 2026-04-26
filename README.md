# 🏥 ClinicEase Pakistan

**An AI-powered prescription reader built for Pakistani patients and pharmacists.**

Doctors' handwriting is notoriously hard to read — in Pakistan, this causes patients to misunderstand their prescriptions and pharmacists to dispense the wrong medicine. ClinicEase solves this by letting anyone photograph a prescription and instantly get a clean, structured, Urdu-translated summary powered by a Vision LLM.

---

## ✨ Features

- 📸 **Prescription Scanning** — Upload any photo of a prescription (handwritten or printed)
- 🤖 **AI Extraction** — Powered by Llama 4 Scout Vision via Groq API; extracts patient info, medicines, dosage, diagnosis, vitals, and more
- 🇵🇰 **Urdu Translation** — Full prescription summary translated into plain Nastaliq Urdu for patients
- 💊 **Medicine Details** — Tap any medicine for category, usage, side effects, precautions, and storage info
- 📄 **PDF Export** — Download a clean, formatted prescription report to share with family or the pharmacy
- 🌐 **Supports English + Urdu + Mixed prescriptions**

---

## 🖥️ Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python / Flask |
| Vision LLM | Groq API — `meta-llama/llama-4-scout-17b-16e-instruct` |
| Text LLM | Groq API — `llama-3.3-70b-versatile` |
| PDF Generation | ReportLab |
| Frontend | HTML / CSS / JavaScript (Jinja2 templates) |

---

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed:

- **Python 3.9+** — [Download here](https://www.python.org/downloads/)
- **pip** (comes with Python)
- A free **Groq API key** — [Get one here](https://console.groq.com)

---

### 1. Clone the Repository

```bash
git clone https://github.com/saadbooran/ClinicEase-Pakistan-APP.git
cd ClinicEase-Pakistan-APP
```

---

### 2. Create a Virtual Environment (Recommended)

```bash
# Create the virtual environment
python -m venv venv

# Activate it — Windows
venv\Scripts\activate

# Activate it — macOS / Linux
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:

| Package | Version | Purpose |
|---------|---------|---------|
| `flask` | 3.0.3 | Web framework |
| `groq` | 1.2.0 | Groq LLM API client |
| `python-dotenv` | 1.0.1 | Load environment variables |
| `Pillow` | 10.4.0 | Image processing |
| `reportlab` | 4.2.2 | PDF generation |
| `Werkzeug` | 3.0.4 | Flask utility |

---

### 4. Set Up Environment Variables

Copy the example env file:

```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

Open `.env` and add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

> 💡 Get your free API key at [https://console.groq.com](https://console.groq.com)

---

### 5. Run the App

```bash
python app.py
```

You should see:

```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

Open your browser and go to **http://127.0.0.1:5000**

---

## 📁 Project Structure

```
ClinicEase-Pakistan-APP/
│
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
│
└── templates/
    └── index.html          # Frontend UI
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Main UI |
| `POST` | `/analyze` | Upload prescription image → returns structured JSON |
| `POST` | `/translate-urdu` | Translate extracted data to Urdu |
| `POST` | `/medicine-detail` | Get detailed info about a medicine |
| `POST` | `/download-pdf` | Generate and download prescription PDF |

---

## 📷 Supported Image Formats

`PNG` · `JPG` · `JPEG` · `WEBP`

---

## ⚠️ Medical Disclaimer

This tool is for **informational purposes only** and does not replace professional medical advice. Always follow your doctor's original prescription. Do not make medical decisions based solely on AI output.

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

1. Fork the repo
2. Create your feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📬 Contact

**Muhammad Saad**
- GitHub: [@saadbooran](https://github.com/saadbooran)

---

## ⭐ Show Your Support

If you find this project useful, please consider giving it a **star** on GitHub — it helps others find the project!

[![GitHub stars](https://img.shields.io/github/stars/saadbooran/ClinicEase-Pakistan-APP?style=social)](https://github.com/saadbooran/ClinicEase-Pakistan-APP)
