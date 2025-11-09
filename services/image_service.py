"""
Service để tạo ảnh từ HTML
"""
import os
import uuid
from html2image import Html2Image
from config import IMAGE_WIDTH, IMAGE_HEIGHT


def generate_image_from_html(html_content: str) -> bytes:
    """
    Tạo ảnh PNG từ HTML content
    
    Args:
        html_content: HTML string
        
    Returns:
        bytes: Ảnh PNG dạng binary
        
    Raises:
        Exception: Nếu có lỗi khi tạo ảnh
    """
    hti = Html2Image()
    
    # Thiết lập size để đảm bảo render đúng kích thước
    hti.size = (IMAGE_WIDTH, IMAGE_HEIGHT)
    
    # Tạo tên file tạm unique
    temp_filename = f"temp_{uuid.uuid4().hex}.png"
    
    try:
        # Tạo ảnh từ HTML với size cố định
        # Sử dụng size parameter để ép đúng kích thước
        hti.screenshot(
            html_str=html_content,
            save_as=temp_filename,
            size=(IMAGE_WIDTH, IMAGE_HEIGHT)
        )
        
        # Đọc file và xóa
        try:
            with open(temp_filename, "rb") as f:
                image_data = f.read()
            os.remove(temp_filename)
            return image_data
        except Exception as e:
            # Đảm bảo xóa file nếu có lỗi
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
            raise Exception(f"Lỗi khi đọc file ảnh: {str(e)}")
            
    except Exception as e:
        # Đảm bảo xóa file nếu có lỗi
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
        raise Exception(f"Lỗi khi tạo ảnh: {str(e)}")

