"""
Request models cho API
"""
from pydantic import BaseModel, Field
from typing import Optional, Literal


class ImageRequest(BaseModel):
    """Model cho request tạo ảnh"""
    category_name: str
    category_bg_color: str
    category_text_color: str
    content: str  # HTML string
    background_theme: str
    logo_url: Optional[str] = None
    show_logo: bool = True
    textAlign: Optional[Literal["left", "right", "center"]] = Field(
        default=None,
        description="Vị trí text: left, right, hoặc center. Nếu không truyền sẽ random."
    )

