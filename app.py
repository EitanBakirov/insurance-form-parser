import streamlit as st
from services.document_ocr import analyze_layout
from services.openai_helpers import init_openai_client, detect_language, extract_form_data
from services.config import DOCUMENT_ENDPOINT, DOCUMENT_KEY, OPENAI_ENDPOINT, OPENAI_KEY
import json

st.set_page_config(page_title="Form Parser", layout="wide")
st.title("🧾 Form Parser: Azure OCR + GPT")

uploaded_file = st.file_uploader("Upload PDF or Image", type=["pdf", "jpg", "jpeg", "png"])

if uploaded_file:
    st.info("Processing document...")

    # Step 1: OCR with Azure Document Intelligence
    result, full_text = analyze_layout(
        file_object=uploaded_file,
        endpoint=DOCUMENT_ENDPOINT, 
        key=DOCUMENT_KEY
    )

    # Step 2: Init OpenAI
    openai_client = init_openai_client(OPENAI_ENDPOINT, OPENAI_KEY)

    # Step 3: Detect language
    language = detect_language(full_text, openai_client)
    st.success(f"Detected language: {language}")

    # Step 4: Extract structured form data via GPT
    form_data = extract_form_data(full_text, language, openai_client)

    # Display result
    st.subheader("📋 Extracted Form Data")
    st.json(form_data)


