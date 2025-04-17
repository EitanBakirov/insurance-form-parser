"""
Azure OpenAI helper functions for language detection and form data extraction.
Handles template loading and GPT-based text processing.
"""

from services.logger_config import logging
from openai import AzureOpenAI
from openai import OpenAIError
from services.config import OPENAI_MODEL, OPENAI_TEMPERATURE
import json
import os

logger = logging.getLogger(__name__)

def init_openai_client(endpoint: str, api_key: str, api_version: str = "2023-07-01-preview") -> AzureOpenAI:
    """
    Initialize Azure OpenAI client.
    
    Args:
        endpoint: Azure OpenAI endpoint URL
        api_key: Azure OpenAI API key
        api_version: API version string
    """
    return AzureOpenAI(azure_endpoint=endpoint, api_key=api_key, api_version=api_version)

def detect_language(text: str, openai_client: AzureOpenAI) -> str:
    """
    Detect if text is Hebrew or English using GPT.
    
    Args:
        text: Input text to analyze
        openai_client: Initialized OpenAI client
    
    Returns:
        str: 'Hebrew' or 'English'
    """
    logger.info("Starting language detection")
    try:
        # Load system prompt from file
        templates_dir = os.path.join(os.path.dirname(__file__), "templates")
        prompt_path = os.path.join(templates_dir, "language_detection_prompt.txt")

        with open(prompt_path, "r", encoding="utf-8") as f:
            system_prompt = f.read().strip()

        # Query OpenAI
        response = openai_client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{text[:1000]}"}
            ],
            temperature=OPENAI_TEMPERATURE
        )
        language = response.choices[0].message.content.strip()

        if language not in ["Hebrew", "English"]:
            raise ValueError("Language must be either 'Hebrew' or 'English")
        
        logger.info(f"Language detected: {language}")
        return language
    
    except OpenAIError as e:
        logger.error(f"OpenAI API error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in detect_language: {e}")
        raise

def load_template_and_prompt(language: str) -> tuple[str, dict]:
    """
    Load language-specific template and system prompt.
    
    Args:
        language: 'Hebrew' or 'English'
    
    Returns:
        tuple: (system_prompt, template_dict)
    """
    try:
        templates_dir = os.path.join(os.path.dirname(__file__), "templates")
        system_prompt_path = os.path.join(templates_dir, "prompt.txt")

        if language == "Hebrew":
            template_path = os.path.join(templates_dir, "hebrew_template.json")
        else:
            template_path = os.path.join(templates_dir, "english_template.json")

        with open(system_prompt_path, "r", encoding="utf-8") as prompt_file:
            system_prompt = prompt_file.read().strip()

        with open(template_path, "r", encoding="utf-8") as template_file:
            template = json.load(template_file)

        return system_prompt, template
    
    except FileNotFoundError as e:
        logger.error(f"Template or prompt file not found: {e}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON template: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in load_template_and_prompt: {e}")
        raise

def extract_form_data(text: str, language: str, openai_client: AzureOpenAI) -> dict:
    """
    Extract structured form data using GPT.
    
    Args:
        text: Input text to process
        language: 'Hebrew' or 'English'
        openai_client: Initialized OpenAI client
    
    Returns:
        dict: Extracted form fields and values
    """
    try:
        
        system_prompt, template = load_template_and_prompt(language)
        
        response = openai_client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Text:\n{text}\n\nJSON template:\n{json.dumps(template, ensure_ascii=False)}"}
            ],
            temperature=OPENAI_TEMPERATURE,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except OpenAIError as e:
        logger.error(f"OpenAI API error in extract_form_data: {e}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding GPT response: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in extract_form_data: {e}")
        raise

def postprocess_ocr(text: str, filepath: str = "services/unecessary_words.txt") -> str:
    """
    Remove unnecessary words from OCR text.
    
    Args:
        text: Input OCR text
        filepath: Path to file containing unnecessary words
    
    Returns:
        str: Processed text
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

