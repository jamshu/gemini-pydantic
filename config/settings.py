"""Configuration management for the Gemini-Pydantic application."""

import os
from dotenv import load_dotenv
from typing import Optional

class Settings:
    """Application settings and configuration."""
    
    def __init__(self):
        """Initialize settings by loading environment variables."""
        load_dotenv()
        self._api_key: Optional[str] = None
        self._validate_config()
    
    def _validate_config(self) -> None:
        """Validate that required configuration is present."""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in environment variables. "
                "Please create a .env file with your API key."
            )
        self._api_key = api_key
    
    @property
    def api_key(self) -> str:
        """Get the Gemini API key."""
        if not self._api_key:
            raise ValueError("API key not configured")
        return self._api_key
    
    @property
    def model_name(self) -> str:
        """Get the Gemini model name."""
        return os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    
    @property
    def max_tokens(self) -> int:
        """Get maximum tokens for API requests."""
        return int(os.getenv("MAX_TOKENS", "1000"))
    
    @property
    def output_dir(self) -> str:
        """Get output directory for generated files."""
        return os.getenv("OUTPUT_DIR", "output")

# Global settings instance
settings = Settings()