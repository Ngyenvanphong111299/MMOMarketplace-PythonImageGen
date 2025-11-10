"""
Service để tạo HTML content
"""
import random
from typing import Optional, Tuple
from services.pexels_service import get_pexels_image
from services.logo_service import get_logo_base64
from app.config import settings

# Default fallback image
DEFAULT_BACKGROUND_IMAGE = "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&h=1200&fit=crop"


def generate_html(
    category_name: str,
    category_bg_color: str,
    category_text_color: str,
    content: str,
    background_theme: str,
    logo_url: Optional[str] = None,
    show_logo: bool = True
) -> str:
    """
    Tạo HTML content từ các tham số
    
    Args:
        category_name: Tên danh mục
        category_bg_color: Màu nền danh mục
        category_text_color: Màu chữ danh mục
        content: Nội dung HTML
        background_theme: Chủ đề để tìm ảnh từ Pexels
        logo_url: URL logo (optional)
        show_logo: Hiển thị logo hay không
        
    Returns:
        HTML string
    """
    # Lấy ảnh từ Pexels
    image_info = get_pexels_image(background_theme)
    
    if image_info:
        image_url = image_info['url']
    else:
        image_url = DEFAULT_BACKGROUND_IMAGE
    
    # Random vị trí text: left, center, right
    text_position = random.choice(["left", "center", "right"])
    
    # Góc xoay dựa trên vị trí text
    if text_position == "left":
        rotate_angle = -4
    elif text_position == "right":
        rotate_angle = 4
    else:  # center
        rotate_angle = 0
    
    # Xử lý logo
    logo_html = ""
    if show_logo:
        logo_src, _ = get_logo_base64(logo_url)
        if logo_src:
            logo_html = f'<img src="{logo_src}" alt="Watermark" />'
    
    # Tạo style động cho text container dựa trên vị trí
    text_container_style, text_bg_style = _get_text_styles(text_position, rotate_angle)
    
    html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=1280, height=850, initial-scale=1.0" />
  <title>Image Generator</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@800;900&family=Roboto:wght@700;900&display=swap');
    
    * {{
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }}
    
    html {{
      width: 1280px;
      height: 850px;
      overflow: visible;
      display: block;
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }}
    
    body {{
      margin: 0;
      padding: 0;
      width: 1280px;
      height: 850px;
      min-height: 850px;
      position: relative;
      overflow: visible;
      font-family: 'Inter', 'Roboto', sans-serif;
      display: block;
      box-sizing: border-box;
    }}
    
    /* Background image */
    .background-image {{
      position: absolute;
      top: 0;
      left: 0;
      width: 1280px;
      height: 850px;
      object-fit: cover;
      object-position: center 30%;
      z-index: 0;
    }}
    
    /* Overlay để background chìm xuống */
    .overlay {{
      position: absolute;
      top: 0;
      left: 0;
      width: 1280px;
      height: 850px;
      background: linear-gradient(
        to bottom,
        rgba(0, 0, 0, 0.3) 0%,
        rgba(0, 0, 0, 0.5) 50%,
        rgba(0, 0, 0, 0.75) 100%
      );
      z-index: 1;
    }}
    
    /* Container cho text - vị trí động */
    .text-container {{
      position: absolute;
      padding: 40px 50px;
      z-index: 2;
      display: flex;
      flex-direction: column;
      gap: 12px;
      width: 100%;
      transform-origin: center center;
      box-sizing: border-box;
    }}
    
    /* Text container align left */
    .text-container.text-left {{
      align-items: flex-start;
    }}
    
    /* Text container align right */
    .text-container.text-right {{
      align-items: flex-end;
    }}
    
    /* Text container align center */
    .text-container.text-center {{
      align-items: center;
    }}
    
    /* Title chính - lớn và nổi bật */
    .main-title {{
      font-size: 30px;
      font-weight: 900;
      line-height: 1.05;
      color: #FFFFFF;
      text-shadow: 
        -3px -3px 0 #000000,
        3px -3px 0 #000000,
        -3px 3px 0 #000000,
        3px 3px 0 #000000,
        0 0 30px rgba(0, 0, 0, 0.9),
        0 6px 12px rgba(0, 0, 0, 0.8);
      letter-spacing: 1px;
      margin: 0;
      text-transform: uppercase;
    }}
    
    /* Subtitle - nhỏ hơn một chút */
    .subtitle {{
      font-size: 38px;
      font-weight: 700;
      line-height: 1.3;
      color: #FFFFFF;
      text-shadow: 
        -2px -2px 0 #000000,
        2px -2px 0 #000000,
        -2px 2px 0 #000000,
        2px 2px 0 #000000,
        0 0 20px rgba(0, 0, 0, 0.8),
        0 4px 10px rgba(0, 0, 0, 0.7);
      letter-spacing: 1px;
      margin: 0;
      text-transform: uppercase;
      margin-top: 8px;
    }}
    
    /* Highlight text với gradient - CHATGPT to và nổi bật hơn */
    .highlight {{
      background: linear-gradient(135deg, #00D9FF 0%, #00B8E6 50%, #0099CC 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      font-size: 1.3em;
      font-weight: 900;
      letter-spacing: 3px;
      position: relative;
      display: inline-block;
      text-shadow: none;
      filter: drop-shadow(0 0 20px rgba(0, 217, 255, 0.7)) 
              drop-shadow(0 0 35px rgba(0, 184, 230, 0.5))
              drop-shadow(0 6px 20px rgba(0, 0, 0, 0.9));
    }}
    
    .highlight::before {{
      content: attr(data-text);
      position: absolute;
      left: 0;
      top: 0;
      z-index: -1;
      background: linear-gradient(135deg, #00D9FF 0%, #00B8E6 50%, #0099CC 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      filter: blur(15px);
      opacity: 0.7;
    }}
    
    /* Background box cho text để nổi bật hơn - vị trí động */
    .text-background {{
      position: absolute;
      z-index: 1;
      pointer-events: none;
    }}
    
    /* Watermark logo - trong text container */
    .watermark-logo {{
      position: relative;
      width: 180px;
      height: 180px;
      min-width: 180px;
      min-height: 180px;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 0;
    }}
    
    .watermark-logo img {{
      width: 100%;
      height: 100%;
      max-width: 100%;
      max-height: 100%;
      object-fit: contain;
      display: block;
    }}
    
    /* Category badge - trong text container */
    .category-badge {{
      width: fit-content;
      position: relative;
      background: {category_bg_color};
      color: {category_text_color};
      padding: 12px 24px;
      border-radius: 8px;
      font-size: 18px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 2px;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
      font-family: 'Inter', 'Roboto', sans-serif;
      margin-bottom: 20px;
    }}
  </style>
</head>
<body>
  <img src="{image_url}" alt="Background" class="background-image" />
  <div class="overlay"></div>
  <div class="text-background" style="{text_bg_style}"></div>
  <div class="text-container text-{text_position}" style="{text_container_style}">
    <div class="category-badge">{category_name}</div>
    <div class="main-title">
      {content}
    </div>
    {f'<div class="watermark-logo">{logo_html}</div>' if logo_html else ''}
  </div>
  <!-- Marker ở cuối để đảm bảo render đầy đủ viewport 850px -->
  <div style="position: absolute; bottom: 0; left: 0; width: 1280px; height: 5px; z-index: 9999; background: transparent; pointer-events: none;"></div>
</body>
</html>"""
    
    return html_content


def _get_text_styles(text_position: str, rotate_angle: int) -> Tuple[str, str]:
    """
    Tạo style cho text container và background dựa trên vị trí
    
    Args:
        text_position: Vị trí text (left, center, right)
        rotate_angle: Góc xoay
        
    Returns:
        tuple (text_container_style, text_bg_style)
    """
    if text_position == "left":
        text_container_style = f"""
      top: 50%;
      left: 5%;
      transform: translateY(-50%) rotate({rotate_angle}deg);
      text-align: left;
      max-width: 60%;
    """
        text_bg_style = """
      top: 50%;
      left: 0;
      transform: translateY(-50%);
      width: 50%;
      height: 100%;
      background: linear-gradient(
        to right,
        rgba(0, 0, 0, 0.7) 0%,
        rgba(0, 0, 0, 0.4) 60%,
        transparent 100%
      );
    """
    elif text_position == "right":
        text_container_style = f"""
      top: 50%;
      right: 5%;
      left: auto;
      transform: translateY(-50%) rotate({rotate_angle}deg);
      text-align: right;
      max-width: 60%;
    """
        text_bg_style = """
      top: 50%;
      right: 0;
      left: auto;
      transform: translateY(-50%);
      width: 50%;
      height: 100%;
      background: linear-gradient(
        to left,
        rgba(0, 0, 0, 0.7) 0%,
        rgba(0, 0, 0, 0.4) 60%,
        transparent 100%
      );
    """
    else:  # center
        text_container_style = f"""
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      text-align: center;
      max-width: 90%;
    """
        text_bg_style = """
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 100%;
      height: 100%;
      background: radial-gradient(
        ellipse at center,
        rgba(0, 0, 0, 0.6) 0%,
        rgba(0, 0, 0, 0.4) 40%,
        transparent 70%
      );
    """
    
    return text_container_style, text_bg_style

