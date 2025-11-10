"""
Service để tạo ảnh từ HTML
"""
import os
import uuid
import logging
from html2image import Html2Image
from PIL import Image

# Image dimensions
IMAGE_WIDTH = 1280
IMAGE_HEIGHT = 850

# Thiết lập logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
    import os
    
    hti = Html2Image()
    
    # Hardcode Chrome/Chromium path - sử dụng wrapper script cho Docker
    wrapper_path = "/usr/local/bin/chromium-wrapper.sh"
    chrome_path = "/usr/bin/chromium"
    
    # Ưu tiên sử dụng wrapper script nếu có, nếu không dùng chrome_path trực tiếp
    if os.path.exists(wrapper_path):
        hti.browser_executable = wrapper_path
    elif os.path.exists(chrome_path):
        hti.browser_executable = chrome_path
    
    # Thiết lập output path (thư mục hiện tại)
    hti.output_path = os.getcwd()
    
    # Thiết lập size để đảm bảo render đúng kích thước
    hti.size = (IMAGE_WIDTH, IMAGE_HEIGHT)
    
    # Tạo tên file tạm unique
    temp_filename = f"temp_{uuid.uuid4().hex}.png"
    temp_filepath = os.path.join(hti.output_path, temp_filename)
    
    try:
        # Tạo ảnh từ HTML với size cố định
        # Lưu HTML vào file tạm để đảm bảo render đầy đủ
        import tempfile as tf
        with tf.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as temp_html:
            temp_html.write(html_content)
            temp_html_path = temp_html.name
        
        try:
            # Screenshot với size cố định
            hti.screenshot(
                html_file=temp_html_path,
                save_as=temp_filename,
                size=(IMAGE_WIDTH, IMAGE_HEIGHT)
            )
            
            # Kiểm tra file ảnh đã tạo và crop transparent borders
            if os.path.exists(temp_filepath):
                # Sử dụng full path
                temp_filename = temp_filepath
                # Crop transparent borders bằng Pillow và resize về 1280x720
                try:
                    img = Image.open(temp_filename).convert("RGBA")
                    bbox = img.getbbox()  # Tự động phát hiện vùng có pixel khác transparent
                    
                    if bbox:
                        # Crop transparent borders
                        cropped = img.crop(bbox)
                        cropped_size = cropped.size
                        
                        # Resize về đúng target size (1280x720)
                        TARGET_WIDTH = 1280
                        TARGET_HEIGHT = 720
                        
                        if cropped_size != (TARGET_WIDTH, TARGET_HEIGHT):
                            # Resize về đúng target size
                            final_img = cropped.resize((TARGET_WIDTH, TARGET_HEIGHT), Image.Resampling.LANCZOS)
                            final_img.save(temp_filename, format='PNG')
                            cropped.close()
                            final_img.close()
                        else:
                            cropped.save(temp_filename, format='PNG')
                            cropped.close()
                        img.close()
                    else:
                        # Không có gì để crop, resize về target size nếu cần
                        TARGET_WIDTH = 1280
                        TARGET_HEIGHT = 720
                        if img.size != (TARGET_WIDTH, TARGET_HEIGHT):
                            final_img = img.resize((TARGET_WIDTH, TARGET_HEIGHT), Image.Resampling.LANCZOS)
                            final_img.save(temp_filename, format='PNG')
                            final_img.close()
                        img.close()
                except Exception as e:
                    logger.warning(f"Could not crop/resize transparent borders: {e}")
        finally:
            # Xóa file HTML tạm
            if os.path.exists(temp_html_path):
                os.remove(temp_html_path)
        
        # Đọc file và xóa
        try:
            # Sử dụng temp_filepath nếu đã được set, nếu không dùng temp_filename
            file_to_read = temp_filepath if 'temp_filepath' in locals() else temp_filename
            if os.path.exists(file_to_read):
                with open(file_to_read, "rb") as f:
                    image_data = f.read()
                os.remove(file_to_read)
                return image_data
            else:
                raise Exception(f"File ảnh không tồn tại: {file_to_read}")
        except Exception as e:
            # Đảm bảo xóa file nếu có lỗi
            file_to_remove = temp_filepath if 'temp_filepath' in locals() else temp_filename
            if os.path.exists(file_to_remove):
                os.remove(file_to_remove)
            raise Exception(f"Lỗi khi đọc file ảnh: {str(e)}")
            
    except Exception as e:
        # Đảm bảo xóa file nếu có lỗi
        file_to_remove = temp_filepath if 'temp_filepath' in locals() else temp_filename
        if os.path.exists(file_to_remove):
            os.remove(file_to_remove)
        raise Exception(f"Lỗi khi tạo ảnh: {str(e)}")

