## 🧾 National Insurance Form Parser

A microservice-based Streamlit app that extracts structured JSON data from scanned ביטוח לאומי (National Insurance Institute) forms using:

- 🧠 **Azure Document Intelligence** (OCR)
- 🤖 **Azure OpenAI (GPT-4o)** for field extraction
- 🌍 Supports Hebrew and English forms
- 🐳 Dockerized with Docker & Docker Compose

---

## 📦 Features

- Upload PDF/JPG scanned forms
- Auto-detects language (Hebrew/English)
- Extracts structured JSON (with fallback for missing fields)
- `.env`-based secret management
- Fully containerized and production-ready

---

## 🧰 Tech Stack

- **Python 3.10**
- **Streamlit** (UI)
- **Azure Document Intelligence**
- **Azure OpenAI (GPT-4o / GPT-4o-mini)**
- **Docker** & **Docker Compose**
- **python-dotenv** for secret loading

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/EitanBakirov/national-insurance-form-parser.git
cd national-insurance-form-parser
```

### 2. Configure environment

```bash
cp .env.example .env
```

Then open `.env` and fill in your **Azure API credentials**:

```env
DOCUMENT_ENDPOINT=https://<your-doc-endpoint>.cognitive.microsoft.com/
DOCUMENT_KEY=your-doc-key

OPENAI_ENDPOINT=https://<your-openai-endpoint>.openai.azure.com/
OPENAI_KEY=your-openai-key
```

---

## 🧪 Run Locally

### Option 1: Using Python (virtualenv)

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
streamlit run app.py
```

---

### Option 2: Using Docker

```bash
docker build -t national_insurance_parser .
docker run --env-file .env -p 8501:8501 national_insurance_parser
```

---

### Option 3: Using Docker Compose (recommended)

```bash
docker-compose up --build
```

Then visit: [http://localhost:8501](http://localhost:8501)

---

## 📝 Example Output

```json
{
  "lastName": "Cohen",
  "firstName": "Avi",
  "idNumber": "123456789",
  "dateOfBirth": {
    "day": "05",
    "month": "06",
    "year": "1984"
  },
  ...
}
```

---

## 🛡️ Security Notes

- ❌ Never commit your `.env` file.
- ✅ Use `.env.example` as a template.
- 🔑 Each developer can configure their own credentials for local runs.

---

## 📁 Project Structure

```
.
├── app.py                    # Streamlit entry point
├── docker-compose.yml
├── Dockerfile
├── .env.example              # Sample environment config
├── requirements.txt
├── services/
│   ├── config.py             # Loads secrets
│   ├── document_ocr.py       # Azure Document Intelligence logic
│   └── openai_helpers.py     # GPT-based field extraction
```
```
