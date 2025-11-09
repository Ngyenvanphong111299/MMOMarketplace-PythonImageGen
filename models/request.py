"""
Request models cho API
"""
from pydantic import BaseModel
from typing import Optional


class ImageRequest(BaseModel):
    """Model cho request tạo ảnh"""
    category_name: str
    category_bg_color: str
    category_text_color: str
    content: str  # HTML string
    background_theme: str
    logo_url: Optional[str] = None
    show_logo: bool = True

