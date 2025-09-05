"""Utilities for cleaning JSON responses from LLMs."""

import json
from typing import Any, Dict

class JSONCleaner:
    """Utility class for cleaning and validating JSON responses."""
    
    @staticmethod
    def clean_json_response(response_text: str) -> str:
        """Remove markdown formatting from JSON response."""
        if not response_text:
            raise ValueError("Response text is empty")
        
        cleaned = response_text.strip()
        
        # Remove common markdown JSON block formatting
        if cleaned.startswith('```json'):
            cleaned = cleaned[7:]  # Remove ```json
        elif cleaned.startswith('```'):
            cleaned = cleaned[3:]   # Remove ```
            
        if cleaned.endswith('```'):
            cleaned = cleaned[:-3]  # Remove trailing ```
        
        return cleaned.strip()
    
    @staticmethod
    def validate_json_structure(json_string: str) -> Dict[str, Any]:
        """Validate that the string is valid JSON and return parsed dict."""
        try:
            parsed = json.loads(json_string)
            if not isinstance(parsed, dict):
                raise ValueError("JSON must be an object, not an array or primitive")
            return parsed
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {e}")
    
    @staticmethod
    def clean_and_validate(response_text: str) -> Dict[str, Any]:
        """Clean JSON response and validate structure in one step."""
        cleaned = JSONCleaner.clean_json_response(response_text)
        return JSONCleaner.validate_json_structure(cleaned)