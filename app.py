"""
National Insurance Form Parser
A Streamlit web application for extracting structured data from insurance forms
using Azure Document Intelligence OCR and Azure OpenAI GPT.
"""

import streamlit as st
from services.document_ocr import analyze_layout, postprocess_ocr
from services.openai_helpers import init_openai_client, detect_language, extract_form_data
from services.config import DOCUMENT_ENDPOINT, DOCUMENT_KEY, OPENAI_ENDPOINT, OPENAI_KEY
from services.validation import validate_completeness
from services.logger_config import logging
from services.monitoring import monitoring
import json
import time

logger = logging.getLogger(__name__)

# Configure Streamlit page settings
st.set_page_config(page_title="Form Parser", layout="wide")
st.title("🧾 Form Parser: Azure OCR + GPT")

# File upload component
uploaded_file = st.file_uploader("Upload PDF or Image", type=["pdf", "jpg", "jpeg", "png"])

# Main file operations and API calls
if uploaded_file:
    start_time = time.time()
    logger.info(f"Processing uploaded file: {uploaded_file.name}")
    try:
        st.info("Processing document...")

        # Step 1: OCR with Azure Document Intelligence
        ocr_start = time.time()
        result, full_text, avg_confidence = analyze_layout(
            file_object=uploaded_file,
            endpoint=DOCUMENT_ENDPOINT, 
            key=DOCUMENT_KEY
        )
        ocr_duration = (time.time() - ocr_start) * 1000
        monitoring.log_api_call("azure_ocr", ocr_duration, success=True)

        # Post-process OCR results
        full_text = postprocess_ocr(full_text, filepath="services/unecessary_words.txt")

        st.write(f"🔍 **Average OCR Word Confidence**: {avg_confidence:.2f}")

        # Step 2: Init OpenAI
        openai_client = init_openai_client(OPENAI_ENDPOINT, OPENAI_KEY)

        # Step 3: Detect language
        gpt_start = time.time()
        language = detect_language(full_text, openai_client)
        st.success(f"Detected language: {language}")

        # Step 4: Extract structured form data via GPT
        form_data = extract_form_data(full_text, language, openai_client)
        gpt_duration = (time.time() - gpt_start) * 1000
        monitoring.log_api_call("openai", gpt_duration, success=True)

        # Step 5: Validate completeness
        validation_result = validate_completeness(form_data)

        # Log overall metrics
        total_duration = (time.time() - start_time) * 1000
        monitoring.log_document_processing(
            ocr_confidence=avg_confidence,
            form_completeness=validation_result["completeness_score"],
            duration_ms=total_duration
        )

        # Split layout into two columns
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📋 Extracted Form Data")
            st.json(form_data)

        with col2:
            st.subheader("✅ Validation Summary")
            st.write(f"🧮 **Completeness Score:** {validation_result['completeness_score'] * 100:.0f}% ({validation_result['total_fields']-validation_result['missing_count']}/{validation_result['total_fields']})")
            if validation_result["missing_fields"]:
                st.warning(f"❗ **Missing Fields** ({validation_result['missing_count']}):")
                for field in validation_result["missing_fields"]:
                    st.markdown(f"- `{field}`")
            else:
                st.success("🎉 All required fields are filled!")

        logger.info("Document processing completed successfully")

    except Exception as e:
        monitoring.log_error(
            error_type=type(e).__name__,
            error_message=str(e)
        )
        st.error(f"Error processing document: {str(e)}")
        logger.error(f"Application error: {e}")



