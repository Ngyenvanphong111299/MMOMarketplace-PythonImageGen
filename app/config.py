"""
Configuration management cho Image Generator API
Hardcoded configuration values
"""
from typing import List


class Settings:
    """Cấu hình ứng dụng - Hardcoded values"""
    
    # API Key Settings - Hardcoded
    API_KEY: str = "XzEcSl7aaW7wfeyxW74IGpGDBcM4noaO"
    API_KEY_HEADER: str = "X-API-Key"
    
    # Rate Limiting Settings - Hardcoded
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    RATE_LIMIT_ENABLED: bool = True
    
    # CORS Settings - Hardcoded
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://localhost:8000",
        "http://localhost:8001",
        "https://api.mavrykpremium.store"
    ]
    ALLOWED_METHODS: List[str] = ["GET", "POST", "OPTIONS"]
    ALLOWED_HEADERS: List[str] = ["Content-Type", "Authorization", "X-API-Key"]
    
    # Security Headers - Hardcoded
    SECURITY_HEADERS_ENABLED: bool = True
    
    # Request Settings - Hardcoded
    MAX_REQUEST_SIZE: int = 10485760  # 10MB
    
    # Logging - Hardcoded
    LOG_LEVEL: str = "INFO"
    SECURITY_LOG_ENABLED: bool = True
    
    # Pexels API - Hardcoded
    PEXELS_API_KEY: str = "EY2W2pV8aA0CN0sJOrPfKOl6osKlxnWnp9gdHo1HfwnaKuELZJHP7BNm"


# Global settings instance
settings = Settings()

