# National Insurance Form Parser

A microservice-based Streamlit application for extracting structured JSON data from scanned Israeli National Insurance (ביטוח לאומי) forms.

The system uses:
- Azure Document Intelligence (OCR)
- Azure OpenAI (GPT-4o) for field extraction
- Hebrew and English support
- Docker and Docker Compose for deployment
- Enhanced logging and monitoring

## Features

- Upload scanned forms (PDF, JPG, PNG)
- Automatic language detection (Hebrew/English)
- Extracts structured data in JSON format
- Handles missing fields and validation
- Uses `.env` for managing secrets
- Comprehensive logging system
- Performance monitoring and metrics
- Containerized and production-ready

## Tech Stack

- Python 3.10
- Streamlit
- Azure Document Intelligence
- Azure OpenAI (GPT-4o / GPT-4o-mini)
- Docker and Docker Compose
- `python-dotenv` for environment variables
- Enhanced logging system with metrics tracking

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/EitanBakirov/national-insurance-form-parser.git
cd national-insurance-form-parser
```

### 2. Configure environment
Copy `.env.example` to `.env` and fill in your Azure credentials.

## Running Options

### Docker Compose (Production)

1. Build and run containers:
```bash
docker compose up --build
```

Access at: http://localhost:8502

### Environment Variables

Required variables in `.env`:
```env
# Azure Document Intelligence
DOCUMENT_ENDPOINT=https://<your-doc-endpoint>.cognitive.microsoft.com/
DOCUMENT_KEY=your-doc-key

# Azure OpenAI
OPENAI_ENDPOINT=https://<your-openai-endpoint>.openai.azure.com/
OPENAI_KEY=your-openai-key
```

## Example Output

```json
{
  "lastName": "Cohen",
  "firstName": "Avi",
  "idNumber": "123456789",
  "dateOfBirth": {
    "day": "05",
    "month": "06",
    "year": "1984"
  }
}
```

## Monitoring & Metrics

The application tracks:
- API performance metrics
  - Success/failure rates
  - Response times
  - Error rates
- Document processing statistics
  - OCR confidence scores
  - Form completion rates
  - Processing durations
- Application health metrics
  - Average processing times
  - Error counts and types
  - Success rates

## Project Structure

```
.
├── app.py                    # Streamlit entry point
├── docker-compose.yml        # Container orchestration
├── Dockerfile               
├── .env.example             # Sample environment config
├── requirements.txt
├── services/
│   ├── config.py            # Environment configuration
│   ├── document_ocr.py      # Azure Document Intelligence
│   ├── openai_helpers.py    # GPT field extraction
│   ├── logger_config.py     # Enhanced logging setup
│   ├── monitoring.py        # Performance monitoring
│   └── validation.py        # Form validation
```

## Potential Upgrades

- **Better OCR Model for Extraction**  
  Improve the accuracy of data extraction by replacing Azure's default OCR with a model trained specifically for Israeli National Insurance forms.  
  If training a model isn't possible, we should use a step-by-step method:
  1. Try to detect known fields and extract the relevant info based on their location on the page.
  2. If that fails, extract text line by line and apply smart rules to find the needed fields.
  3. If needed, pass all text to the LLM and let it try to understand the form.

- **User Editing with Accuracy Feedback**  
  Let users fix any incorrect fields through an easy-to-use form.  
  After they submit, show an **accuracy score** that compares the original extraction to the corrected version.
  
