# 💊 Rx Reader — AI Prescription Interpreter

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)
![Claude AI](https://img.shields.io/badge/Claude-Sonnet_4-D97706?style=for-the-badge&logo=anthropic&logoColor=white)
![Grok AI](https://img.shields.io/badge/Grok-2_Vision-000000?style=for-the-badge&logo=x&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.0-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.10-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![Tesseract](https://img.shields.io/badge/Tesseract-OCR-4CAF50?style=for-the-badge)

**A web app that helps Pakistani patients understand handwritten doctor's prescriptions using AI.**

[Features](#-features) · [Screenshots](#-screenshots) · [Quick Start](#-quick-start) · [Tech Stack](#-tech-stack) · [How It Works](#-how-it-works)

</div>

---

## 🌟 Features

- 📸 **Upload prescription photos** — supports JPG, PNG, WEBP, and more
- 🔍 **OCR + AI extraction** — combines Tesseract OCR with Claude or Grok Vision for high accuracy
- 🤖 **Dual AI Provider** — choose between **Claude (Anthropic)** or **Grok (xAI)** at analysis time
- 💊 **Medicine breakdown** — name, dosage, frequency, duration, special instructions
- 🗣️ **Plain English summaries** — no medical jargon
- 🇵🇰 **Pakistan-aware** — understands Urdu terms, Roman Urdu, and local medical abbreviations (BD, TDS, OD, SOS, etc.)
- 📄 **Download PDF** — professional summary you can share or save
- 📱 **Mobile-friendly** — works on any device
- ⚠️ **Confidence scoring** — tells you how clearly the prescription was read

---

## 📸 Screenshots

> _Add your screenshots here after running the app_

| Upload Screen | Results View | PDF Export |
|:---:|:---:|:---:|
| _(screenshot)_ | _(screenshot)_ | _(screenshot)_ |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Tesseract OCR installed on your system
- At least one API key: [Anthropic (Claude)](https://console.anthropic.com) or [xAI (Grok)](https://console.x.ai)

### 1. Install Tesseract OCR

**Ubuntu / Debian:**
```bash
sudo apt-get install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

**Windows:**
Download the installer from: https://github.com/UB-Mannheim/tesseract/wiki

### 2. Clone the repository

```bash
git clone https://github.com/yourusername/rx-reader.git
cd rx-reader
```

### 3. Create virtual environment & install dependencies

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and add your API key(s):
```env
# At least one is required:
ANTHROPIC_API_KEY=your_anthropic_api_key_here
XAI_API_KEY=your_xai_api_key_here
```

- Get your **Anthropic (Claude)** key at: https://console.anthropic.com
- Get your **xAI (Grok)** key at: https://console.x.ai

### 5. Run the app

```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## 🏗️ Project Structure

```
prescription-reader/
├── app.py                  # Flask backend — routes, OCR, Claude & Grok integration
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── .env                    # Your local env (not committed to git)
├── templates/
│   └── index.html          # Frontend — Tailwind CSS + vanilla JS
├── static/
│   └── css/                # (optional custom CSS)
└── README.md
```

---

## ⚙️ How It Works

```
User uploads photo + selects AI provider (Claude or Grok)
        │
        ▼
  OpenCV Enhancement
  ┌─────────────────────────────────────┐
  │ • Convert to grayscale              │
  │ • Denoise (fastNlMeansDenoising)    │
  │ • Adaptive thresholding             │
  │ • Sharpen kernel                    │
  │ • 2× upscaling for better OCR       │
  └─────────────────────────────────────┘
        │
        ▼
  Tesseract OCR
  ┌─────────────────────────────────────┐
  │ • Multiple PSM modes for best result│
  │ • Raw text extraction               │
  └─────────────────────────────────────┘
        │
        ▼
  Claude Sonnet Vision  OR  Grok-2 Vision
  ┌─────────────────────────────────────┐
  │ • Receives original image + OCR text│
  │ • Interprets garbled/mixed text     │
  │ • Understands Urdu & local context  │
  │ • Returns structured JSON           │
  └─────────────────────────────────────┘
        │
        ▼
  Structured Display + PDF
  ┌─────────────────────────────────────┐
  │ • Patient & doctor info             │
  │ • Medicine cards with dosage        │
  │ • Instructions & follow-up          │
  │ • Downloadable PDF via ReportLab    │
  └─────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.9+, Flask 3.0 |
| **AI / LLM** | Claude Sonnet 4 (Anthropic) · Grok-2 Vision (xAI) |
| **OCR** | Tesseract OCR via pytesseract |
| **Image Processing** | OpenCV, Pillow, NumPy |
| **PDF Generation** | ReportLab |
| **Frontend** | Tailwind CSS 3, Vanilla JavaScript |
| **Env Management** | python-dotenv |

---

## 🔐 Security Notes

- API keys are stored in `.env` — never commit this file
- `.env` is excluded via `.gitignore`
- No prescription data is stored — all processing is in-memory
- Images are sent to Anthropic or xAI depending on the selected provider

---

## ⚕️ Disclaimer

This application is for **informational purposes only**. It does not provide medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional and refer to your original prescription. The AI may make mistakes — especially with unclear handwriting.

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">
Made with ❤️ for Pakistani patients · Powered by Claude AI & Grok AI
</div>

**A web app that helps Pakistani patients understand handwritten doctor's prescriptions using AI.**

[Features](#-features) · [Screenshots](#-screenshots) · [Quick Start](#-quick-start) · [Tech Stack](#-tech-stack) · [How It Works](#-how-it-works)

</div>

---

## 🌟 Features

- 📸 **Upload prescription photos** — supports JPG, PNG, WEBP, and more
- 🔍 **OCR + AI extraction** — combines Tesseract OCR with Claude Vision for high accuracy
- 💊 **Medicine breakdown** — name, dosage, frequency, duration, special instructions
- 🗣️ **Plain English summaries** — no medical jargon
- 🇵🇰 **Pakistan-aware** — understands Urdu terms, Roman Urdu, and local medical abbreviations (BD, TDS, OD, SOS, etc.)
- 📄 **Download PDF** — professional summary you can share or save
- 📱 **Mobile-friendly** — works on any device
- ⚠️ **Confidence scoring** — tells you how clearly the prescription was read

---

## 📸 Screenshots

> _Add your screenshots here after running the app_

| Upload Screen | Results View | PDF Export |
|:---:|:---:|:---:|
| _(screenshot)_ | _(screenshot)_ | _(screenshot)_ |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Tesseract OCR installed on your system
- An [Anthropic API key](https://console.anthropic.com)

### 1. Install Tesseract OCR

**Ubuntu / Debian:**
```bash
sudo apt-get install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

**Windows:**
Download the installer from: https://github.com/UB-Mannheim/tesseract/wiki

### 2. Clone the repository

```bash
git clone https://github.com/yourusername/rx-reader.git
cd rx-reader
```

### 3. Create virtual environment & install dependencies

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and add your Anthropic API key:
```env
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### 5. Run the app

```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## 🏗️ Project Structure

```
prescription-reader/
├── app.py                  # Flask backend — routes, OCR, Claude integration
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── .env                    # Your local env (not committed to git)
├── templates/
│   └── index.html          # Frontend — Tailwind CSS + vanilla JS
├── static/
│   └── css/                # (optional custom CSS)
└── README.md
```

---

## ⚙️ How It Works

```
User uploads photo
        │
        ▼
  OpenCV Enhancement
  ┌─────────────────────────────────────┐
  │ • Convert to grayscale              │
  │ • Denoise (fastNlMeansDenoising)    │
  │ • Adaptive thresholding             │
  │ • Sharpen kernel                    │
  │ • 2× upscaling for better OCR       │
  └─────────────────────────────────────┘
        │
        ▼
  Tesseract OCR
  ┌─────────────────────────────────────┐
  │ • Multiple PSM modes for best result│
  │ • Raw text extraction               │
  └─────────────────────────────────────┘
        │
        ▼
  Claude Sonnet Vision + Text
  ┌─────────────────────────────────────┐
  │ • Receives original image + OCR text│
  │ • Interprets garbled/mixed text     │
  │ • Understands Urdu & local context  │
  │ • Returns structured JSON           │
  └─────────────────────────────────────┘
        │
        ▼
  Structured Display + PDF
  ┌─────────────────────────────────────┐
  │ • Patient & doctor info             │
  │ • Medicine cards with dosage        │
  │ • Instructions & follow-up          │
  │ • Downloadable PDF via ReportLab    │
  └─────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.9+, Flask 3.0 |
| **AI / LLM** | Anthropic Claude Sonnet (Vision + Text) |
| **OCR** | Tesseract OCR via pytesseract |
| **Image Processing** | OpenCV, Pillow, NumPy |
| **PDF Generation** | ReportLab |
| **Frontend** | Tailwind CSS 3, Vanilla JavaScript |
| **Env Management** | python-dotenv |

---

## 🔐 Security Notes

- API keys are stored in `.env` — never commit this file
- `.env` is excluded via `.gitignore`
- No prescription data is stored — all processing is in-memory
- Images are only sent to Anthropic's API (subject to their [privacy policy](https://www.anthropic.com/privacy))

---

## ⚕️ Disclaimer

This application is for **informational purposes only**. It does not provide medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional and refer to your original prescription. The AI may make mistakes — especially with unclear handwriting.

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">
Made with ❤️ for Pakistani patients · Powered by Claude AI
</div>
