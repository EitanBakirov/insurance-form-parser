from dataclasses import dataclass
from datetime import datetime
import time
from typing import Dict, Any
from services.logger_config import logger

@dataclass
class ProcessMetrics:
    timestamp: datetime
    process_name: str
    duration_ms: float
    status: str
    details: Dict[str, Any]

class ApplicationMonitoring:
    def __init__(self):
        self.metrics: Dict[str, Any] = {
            "api_calls": {
                "azure_ocr": {"success": 0, "failed": 0, "total_time_ms": 0},
                "openai": {"success": 0, "failed": 0, "total_time_ms": 0}
            },
            "processing": {
                "documents_processed": 0,
                "average_ocr_confidence": 0,
                "average_form_completeness": 0,
                "errors": 0
            },
            "performance": {
                "average_processing_time_ms": 0
            }
        }

    def log_api_call(self, api_name: str, duration_ms: float, success: bool):
        """Log API call metrics"""
        status = "success" if success else "failed"
        self.metrics["api_calls"][api_name][status] += 1
        self.metrics["api_calls"][api_name]["total_time_ms"] += duration_ms
        
        logger.info("API Call Metrics", extra={
            "api_name": api_name,
            "duration_ms": duration_ms,
            "status": status,
            "metrics": self.metrics["api_calls"][api_name]
        })

    def log_document_processing(self, ocr_confidence: float, form_completeness: float, duration_ms: float):
        """Log document processing metrics"""
        self.metrics["processing"]["documents_processed"] += 1
        self.metrics["processing"]["average_ocr_confidence"] = (
            (self.metrics["processing"]["average_ocr_confidence"] * 
             (self.metrics["processing"]["documents_processed"] - 1) + ocr_confidence) /
            self.metrics["processing"]["documents_processed"]
        )
        self.metrics["processing"]["average_form_completeness"] = (
            (self.metrics["processing"]["average_form_completeness"] * 
             (self.metrics["processing"]["documents_processed"] - 1) + form_completeness) /
            self.metrics["processing"]["documents_processed"]
        )
        self.metrics["performance"]["average_processing_time_ms"] = (
            (self.metrics["performance"]["average_processing_time_ms"] * 
             (self.metrics["processing"]["documents_processed"] - 1) + duration_ms) /
            self.metrics["processing"]["documents_processed"]
        )
        
        logger.info("Document Processing Metrics", extra={
            "metrics": self.metrics
        })

    def log_error(self, error_type: str, error_message: str):
        """Log error metrics"""
        self.metrics["processing"]["errors"] += 1
        logger.error(f"Application Error", extra={
            "error_type": error_type,
            "error_message": error_message,
            "total_errors": self.metrics["processing"]["errors"]
        })

monitoring = ApplicationMonitoring()