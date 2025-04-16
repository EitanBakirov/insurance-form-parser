from openai import AzureOpenAI
import json

def init_openai_client(endpoint, api_key, api_version="2023-07-01-preview"):
    return AzureOpenAI(azure_endpoint=endpoint, api_key=api_key, api_version=api_version)

def detect_language(text, openai_client):
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a language detection assistant. Respond with only 'hebrew' or 'english'."},
            {"role": "user", "content": f"{text[:1000]}"}
        ],
        temperature=0
    )
    return response.choices[0].message.content.strip().lower()

def extract_form_data(text, language, openai_client):
    if language == "hebrew":
        template = {
            "שם משפחה": "", "שם פרטי": "", "מספר זהות": "", "מין": "",
            "תאריך לידה": {"יום": "", "חודש": "", "שנה": ""},
            "כתובת": {"רחוב": "", "מספר בית": "", "כניסה": "", "דירה": "", "ישוב": "", "מיקוד": "", "תא דואר": ""},
            "טלפון קווי": "", "טלפון נייד": "", "סוג העבודה": "",
            "תאריך הפגיעה": {"יום": "", "חודש": "", "שנה": ""},
            "שעת הפגיעה": "", "מקום התאונה": "", "כתובת מקום התאונה": "",
            "תיאור התאונה": "", "האיבר שנפגע": "", "חתימה": "",
            "תאריך מילוי הטופס": {"יום": "", "חודש": "", "שנה": ""},
            "תאריך קבלת הטופס בקופה": {"יום": "", "חודש": "", "שנה": ""},
            "למילוי ע\"י המוסד הרפואי": {"חבר בקופת חולים": "", "מהות התאונה": "", "אבחנות רפואיות": ""}
        }
        system_prompt = "אתה עוזר להפיק מידע מטפסים רפואיים. עליך למלא את שדות ה-JSON בהתאם למידע שמופיע בטקסט."
    else:
        template = {
            "lastName": "", "firstName": "", "idNumber": "", "gender": "",
            "dateOfBirth": {"day": "", "month": "", "year": ""},
            "address": {"street": "", "houseNumber": "", "entrance": "", "apartment": "", "city": "", "postalCode": "", "poBox": ""},
            "landlinePhone": "", "mobilePhone": "", "jobType": "",
            "dateOfInjury": {"day": "", "month": "", "year": ""},
            "timeOfInjury": "", "accidentLocation": "", "accidentAddress": "",
            "accidentDescription": "", "injuredBodyPart": "", "signature": "",
            "formFillingDate": {"day": "", "month": "", "year": ""},
            "formReceiptDateAtClinic": {"day": "", "month": "", "year": ""},
            "medicalInstitutionFields": {"healthFundMember": "", "natureOfAccident": "", "medicalDiagnoses": ""}
        }
        system_prompt = "You are an assistant for extracting information from medical forms. Fill in the JSON fields based on the information found in the text."

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Text:\n{text}\n\nJSON template:\n{json.dumps(template, ensure_ascii=False)}"}
        ],
        temperature=0,
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)
