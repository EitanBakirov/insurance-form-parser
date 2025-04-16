## 🧾 National Insurance Form Parser

A microservice-based Streamlit app that extracts structured JSON data from scanned ביטוח לאומי (National Insurance Institute) forms using:

- 🧠 **Azure Document Intelligence** (OCR)
- 🤖 **Azure OpenAI (GPT-4o)** for field parsing
- 🌍 Hebrew or English support
- 🐳 Containerized with Docker & Docker Compose

---

## 📦 Features

- Upload PDF/JPG forms
- Auto-detects language (Hebrew/English)
- Extracts structured JSON (with fallback for missing fields)
- Secure `.env`-based configuration
- Fully dockerized and easy to run anywhere

---

## 🧰 Tech Stack

- **Python 3.10**
- **Streamlit** (UI)
- **Azure Document Intelligence**
- **Azure OpenAI (GPT-4o / GPT-4o-mini)**
- **Docker** & **Docker Compose**
- **dotenv** for secret loading

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-username/national_insurance_form_parser.git
cd national_insurance_form_parser
```

### 2. Configure environment

```bash
cp .env.example .env
```

Then open `.env` and fill in your **Azure API keys**:

```env
DOCUMENT_ENDPOINT=https://<your-doc-endpoint>.cognitive.microsoft.com/
DOCUMENT_KEY=your-doc-key

OPENAI_ENDPOINT=https://<your-openai-endpoint>.openai.azure.com/
OPENAI_KEY=your-openai-key
```

---

## 🧪 Run Locally

### Option 1: With Python virtual environment

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
streamlit run app.py
```

---

### Option 2: With Docker

```bash
docker build -t national_insurance_parser .
docker run --env-file .env -p 8501:8501 national_insurance_parser
```

---

### Option 3: With Docker Compose (recommended)

```bash
docker-compose up --build
```

Visit: [http://localhost:8501](http://localhost:8501)

---

## 📝 Example Output

```json
{
  "lastName": "Cohen",
  "firstName": "Avi",
  "idNumber": "123456789",
  ...
}
```

---

## 🛡️ Security Notes

- Never commit your `.env` file.
- Always use `.env.example` for templates.
- This app supports multiple users by letting each developer insert their own credentials.

---

## 📁 Project Structure

```
.
├── app.py                      # Streamlit entry point
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── services/
│   ├── config.py               # Loads secrets from .env
│   ├── document_ocr.py         # Document Intelligence logic
│   └── openai_helpers.py       # GPT integration
```

