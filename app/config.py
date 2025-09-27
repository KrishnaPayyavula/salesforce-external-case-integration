"""Configuration settings for the Salesforce External Case Integration API."""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Salesforce Configuration
    salesforce_client_id: str
    salesforce_client_secret: str
    salesforce_base_url: str
    salesforce_api_version: str = "v64.0"
    
    # Application Configuration
    app_name: str = "Salesforce External Case Integration"
    app_version: str = "1.0.0"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    
    # OAuth Configuration
    oauth_token_url: str = "/services/oauth2/token"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
