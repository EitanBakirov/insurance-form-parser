"""
Azure Document Intelligence OCR module for text extraction from documents.
Handles PDF and image files, providing text content and confidence scores.
"""

from services.logger_config import logging
from services.monitoring import monitoring
import time

logger = logging.getLogger(__name__)

from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, AnalyzeResult
from azure.core.exceptions import AzureError


def analyze_layout(file_object=None, url=None, endpoint=None, key=None, confidence_threshold=0.8):
    """
    Analyze document layout using Azure Document Intelligence.
    
    Args:
        file_object: File buffer to analyze
        url: URL of document to analyze
        endpoint: Azure endpoint URL
        key: Azure API key
        confidence_threshold: Minimum confidence score (0-1)
    
    Returns:
        tuple: (AnalyzeResult, extracted_text, average_confidence)
    """
    start_time = time.time()
    try:
        logger.info(f"Starting document analysis with confidence threshold: {confidence_threshold}")
        client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))

        if url:
            poller = client.begin_analyze_document(
                model_id="prebuilt-layout",
                analyze_request=AnalyzeDocumentRequest(url_source=url)
            )
        elif file_object:
            poller = client.begin_analyze_document(
                model_id="prebuilt-layout",
                body=file_object
            )
        else:
            raise ValueError("Either 'file_object' or 'url' must be provided.")

        result: AnalyzeResult = poller.result()

        full_text = ""
        total_confidence = 0
        total_words = 0

        for page in result.pages:
            for line in page.lines:
                words = [word for word in page.words if word.span.offset >= line.spans[0].offset and
                         (word.span.offset + word.span.length) <= (line.spans[0].offset + line.spans[0].length)]

                if all(word.confidence >= confidence_threshold for word in words):
                    full_text += line.content + "\n"

                for word in words:
                    total_confidence += word.confidence
                    total_words += 1

        avg_confidence = total_confidence / total_words if total_words > 0 else 0

        logger.info(f"Document analysis completed. Average confidence: {avg_confidence:.2f}")
        duration = (time.time() - start_time) * 1000
        monitoring.log_api_call("azure_ocr", duration, success=True)
        return result, full_text, avg_confidence

    except AzureError as e:
        logger.error(f"Azure OCR error: {e}")
        duration = (time.time() - start_time) * 1000
        monitoring.log_api_call("azure_ocr", duration, success=False)
        raise
    except Exception as e:
        logger.error(f"Unexpected error in analyze_layout: {e}")
        duration = (time.time() - start_time) * 1000
        monitoring.log_api_call("azure_ocr", duration, success=False)
        raise


def postprocess_ocr(text: str, filepath: str = "services/unecessary_words.txt") -> str:
    """
    Removes unnecessary words from the input text based on a file containing one word per line.

    Args:
        text (str): The input text to clean.
        filepath (str): Path to the file containing unnecessary words (one per line).

    Returns:
        str: Cleaned text with unnecessary words removed.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            unnecessary_words = f.read().splitlines()

        for word in unnecessary_words:
            text = text.replace(word, "")

        return text
    except FileNotFoundError:
        logger.error(f"Unnecessary words file not found: {filepath}")
        raise
    except Exception as e:
        logger.error(f"Error in postprocess_ocr: {e}")
        raise