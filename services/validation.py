"""
Form data validation module.
Checks completeness of form fields and calculates validation scores.
"""

from services.logger_config import logging

logger = logging.getLogger(__name__)

def validate_completeness(form_data: dict, required_fields: list[str] = None) -> dict:
    """
    Validate form data completeness and calculate completion score.
    
    Args:
        form_data: Dictionary containing form fields
        required_fields: Optional list of required field paths
    
    Returns:
        dict: Validation results with completeness metrics
    """
    logger.info("Starting form validation")
    try:
        if not isinstance(form_data, dict):
            raise ValueError("form_data must be a dictionary.")

        if required_fields is None:
            # If not passed, auto-detect all keys (recursively)
            required_fields = _flatten_keys(form_data)

        missing = []

        for key_path in required_fields:
            value = _get_nested_value(form_data, key_path)
            if value == "":
                missing.append(key_path)

        completeness_score = round(1 - len(missing) / len(required_fields), 2)
        logger.info(f"Validation complete. Score: {completeness_score}")

        return {
            "total_fields": len(required_fields),
            "missing_fields": missing,
            "missing_count": len(missing),
            "completeness_score": completeness_score
        }
    except Exception as e:
        logger.error(f"Error in validate_completeness: {e}")
        raise


def _flatten_keys(d: dict, parent_key: str = "") -> list[str]:
    """
    Convert nested dictionary keys to dot notation paths.
    Example: {'a': {'b': 1}} -> ['a.b']
    """
    try:
        keys = []
        for k, v in d.items():
            full_key = f"{parent_key}.{k}" if parent_key else k
            if isinstance(v, dict):
                keys += _flatten_keys(v, full_key)
            else:
                keys.append(full_key)
        return keys
    except Exception as e:
        logger.error(f"Error in _flatten_keys: {e}")
        raise


def _get_nested_value(d: dict, key_path: str) -> str:
    """
    Get value from nested dictionary using dot notation path.
    Example: _get_nested_value({'a': {'b': 1}}, 'a.b') -> 1
    """
    try:
        keys = key_path.split(".")
        for key in keys:
            d = d.get(key, {})
        return d if isinstance(d, str) else ""
    except Exception as e:
        logger.error(f"Error in _get_nested_value: {e}")
        raise


def validate_config():
    """
    Validate required environment variables.
    
    Raises:
        EnvironmentError: If any required environment variable is missing
    """
    required_vars = [
        "DOCUMENT_ENDPOINT",
        "DOCUMENT_KEY",
        "OPENAI_ENDPOINT",
        "OPENAI_KEY"
    ]
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")
