"""
Service để xử lý logo
"""
import requests
import base64
import os
from typing import Optional, Tuple


def get_logo_base64(logo_url: Optional[str] = None) -> Tuple[str, str]:
    """
    Lấy logo và convert sang base64.
    
    Args:
        logo_url: URL của logo (optional). Nếu không có sẽ dùng logo local.
        
    Returns:
        tuple (logo_src, logo_ext): logo_src là data URI, logo_ext là extension
    """
    # Nếu có logo_url, download từ URL
    if logo_url:
        try:
            response = requests.get(logo_url, timeout=10)
            response.raise_for_status()
            logo_data = response.content
            
            # Xác định extension từ URL hoặc content-type
            logo_ext = "png"
            if logo_url.lower().endswith(('.webp', '.jpg', '.jpeg')):
                logo_ext = logo_url.split('.')[-1].lower()
            elif 'content-type' in response.headers:
                content_type = response.headers['content-type']
                if 'webp' in content_type:
                    logo_ext = "webp"
                elif 'jpeg' in content_type or 'jpg' in content_type:
                    logo_ext = "jpg"
            
            logo_base64 = base64.b64encode(logo_data).decode('utf-8')
            logo_src = f"data:image/{logo_ext};base64,{logo_base64}"
            return logo_src, logo_ext
        except Exception as e:
            print(f"Loi khi tai logo tu URL: {e}")
            # Fallback về logo local
            pass
    
    # Thử đọc logo local
    logo_path = None
    if os.path.exists("logo.png"):
        logo_path = "logo.png"
        logo_ext = "png"
    elif os.path.exists("logo.webp"):
        logo_path = "logo.webp"
        logo_ext = "webp"
    
    if logo_path:
        try:
            with open(logo_path, "rb") as logo_file:
                logo_data = logo_file.read()
                logo_base64 = base64.b64encode(logo_data).decode('utf-8')
                logo_src = f"data:image/{logo_ext};base64,{logo_base64}"
                return logo_src, logo_ext
        except Exception as e:
            print(f"Loi khi tai logo: {e}")
            return "", ""
    
    return "", ""

