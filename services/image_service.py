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
    import tempfile as tf
    
    hti = Html2Image()
    
    # Hardcode Chrome/Chromium path - sử dụng wrapper script cho Docker
    wrapper_path = "/usr/local/bin/chromium-wrapper.sh"
    chrome_path = "/usr/bin/chromium"
    
    # Kiểm tra và sửa wrapper script nếu cần
    if os.path.exists(wrapper_path):
        # Đọc nội dung wrapper script
        with open(wrapper_path, 'r') as f:
            wrapper_content = f.read()
        # Đảm bảo wrapper script có đầy đủ flags
        if '--no-sandbox' not in wrapper_content or '--disable-dev-shm-usage' not in wrapper_content:
            logger.warning(f"Wrapper script thiếu flags, sẽ tạo lại")
            # Tạo lại wrapper script với đầy đủ flags
            new_wrapper = '#!/bin/bash\nexec /usr/bin/chromium --no-sandbox --disable-dev-shm-usage --disable-gpu --headless --disable-software-rasterizer "$@"\n'
            with open(wrapper_path, 'w') as f:
                f.write(new_wrapper)
            os.chmod(wrapper_path, 0o755)
        hti.browser_executable = wrapper_path
        logger.info(f"Sử dụng wrapper script: {wrapper_path}")
    elif os.path.exists(chrome_path):
        hti.browser_executable = chrome_path
        logger.info(f"Sử dụng chromium trực tiếp: {chrome_path}")
    
    # Thiết lập temp_dir cho Html2Image để lưu file tạm
    # Html2Image cần quyền ghi vào thư mục này
    
    # Tạo thư mục temp nếu chưa có và thiết lập output path
    temp_dir = os.path.join(os.getcwd(), "temp")
    os.makedirs(temp_dir, exist_ok=True)
    hti.output_path = temp_dir
    
    # Thiết lập size để đảm bảo render đúng kích thước
    hti.size = (IMAGE_WIDTH, IMAGE_HEIGHT)
    
    # Tạo tên file tạm unique
    temp_filename = f"temp_{uuid.uuid4().hex}.png"
    temp_filepath = os.path.join(hti.output_path, temp_filename)
    
    # Lưu HTML vào file tạm
    temp_html_path = None
    
    try:
        # Lưu HTML vào file tạm để đảm bảo render đầy đủ
        with tf.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8', dir=temp_dir) as temp_html:
            temp_html.write(html_content)
            temp_html_path = temp_html.name
        
        logger.info(f"Tạo ảnh từ HTML, output path: {hti.output_path}, file: {temp_filename}")
        logger.info(f"HTML file path: {temp_html_path}")
        logger.info(f"Expected image path: {temp_filepath}")
        
        # Screenshot với size cố định - thử dùng html_str trước
        screenshot_paths = None
        import time
        
        try:
            # Thử dùng html_str trực tiếp
            screenshot_paths = hti.screenshot(
                html_str=html_content,
                save_as=temp_filename,
                size=(IMAGE_WIDTH, IMAGE_HEIGHT)
            )
            logger.info(f"Screenshot returned paths: {screenshot_paths}")
        except Exception as screenshot_error:
            logger.warning(f"Screenshot với html_str thất bại: {screenshot_error}, thử với html_file")
            # Fallback: dùng html_file
            try:
                screenshot_paths = hti.screenshot(
                    html_file=temp_html_path,
                    save_as=temp_filename,
                    size=(IMAGE_WIDTH, IMAGE_HEIGHT)
                )
                logger.info(f"Screenshot với html_file returned paths: {screenshot_paths}")
            except Exception as file_error:
                logger.error(f"Screenshot với html_file cũng thất bại: {file_error}")
                raise Exception(f"Không thể tạo screenshot: {file_error}")
        
        # Đợi một chút để đảm bảo file được tạo xong
        # Tăng delay để đảm bảo Chromium hoàn thành việc tạo file
        time.sleep(3)
        
        # Thử đợi file xuất hiện với timeout
        max_wait = 10  # seconds
        wait_interval = 0.5
        waited = 0
        while waited < max_wait:
            if os.path.exists(temp_filepath):
                logger.info(f"File đã xuất hiện sau {waited} giây: {temp_filepath}")
                break
            time.sleep(wait_interval)
            waited += wait_interval
        
        # screenshot() có thể trả về list các đường dẫn file
        if screenshot_paths and len(screenshot_paths) > 0:
            # Lấy đường dẫn đầu tiên nếu có
            actual_path = screenshot_paths[0] if isinstance(screenshot_paths, list) else screenshot_paths
            # Kiểm tra xem đường dẫn có tồn tại không
            if actual_path and os.path.exists(actual_path):
                temp_filepath = actual_path
                logger.info(f"Sử dụng đường dẫn từ screenshot(): {temp_filepath}")
            else:
                # Nếu đường dẫn từ screenshot() không tồn tại, thử normalize path
                if actual_path:
                    normalized_path = os.path.normpath(actual_path)
                    if os.path.exists(normalized_path):
                        temp_filepath = normalized_path
                        logger.info(f"Sử dụng đường dẫn normalized từ screenshot(): {temp_filepath}")
                    else:
                        # Thử với absolute path
                        abs_path = os.path.abspath(actual_path)
                        if os.path.exists(abs_path):
                            temp_filepath = abs_path
                            logger.info(f"Sử dụng absolute path từ screenshot(): {temp_filepath}")
                        else:
                            logger.warning(f"Đường dẫn từ screenshot() không tồn tại: {actual_path}, sẽ tìm ở các vị trí khác")
        
        # Kiểm tra file ảnh đã tạo
        if not os.path.exists(temp_filepath):
            # Thử tìm file ở các vị trí khác có thể
            possible_paths = [
                os.path.join(os.getcwd(), temp_filename),
                os.path.join("/tmp", temp_filename),
                os.path.join(temp_dir, temp_filename),
                temp_filepath
            ]
            # Thêm các đường dẫn từ screenshot() nếu có
            if screenshot_paths:
                if isinstance(screenshot_paths, list):
                    possible_paths.extend(screenshot_paths)
                else:
                    possible_paths.append(screenshot_paths)
            
            found = False
            for path in possible_paths:
                if path and os.path.exists(path):
                    temp_filepath = path
                    found = True
                    logger.info(f"Tìm thấy file ảnh tại: {temp_filepath}")
                    break
            
            if not found:
                # Liệt kê tất cả file trong temp_dir để debug
                try:
                    files_in_temp = os.listdir(temp_dir)
                    logger.error(f"Các file trong temp_dir: {files_in_temp}")
                except:
                    pass
                raise Exception(f"File ảnh không được tạo. Đã kiểm tra: {possible_paths}")
        
        # Crop transparent borders bằng Pillow và resize về 1280x720
        try:
            img = Image.open(temp_filepath).convert("RGBA")
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
                    final_img.save(temp_filepath, format='PNG')
                    cropped.close()
                    final_img.close()
                else:
                    cropped.save(temp_filepath, format='PNG')
                    cropped.close()
                img.close()
            else:
                # Không có gì để crop, resize về target size nếu cần
                TARGET_WIDTH = 1280
                TARGET_HEIGHT = 720
                if img.size != (TARGET_WIDTH, TARGET_HEIGHT):
                    final_img = img.resize((TARGET_WIDTH, TARGET_HEIGHT), Image.Resampling.LANCZOS)
                    final_img.save(temp_filepath, format='PNG')
                    final_img.close()
                img.close()
        except Exception as e:
            logger.warning(f"Could not crop/resize transparent borders: {e}")
        
        # Đọc file và xóa
        if os.path.exists(temp_filepath):
            with open(temp_filepath, "rb") as f:
                image_data = f.read()
            os.remove(temp_filepath)
            logger.info(f"Đã tạo và đọc file ảnh thành công: {temp_filepath}")
            return image_data
        else:
            raise Exception(f"File ảnh không tồn tại sau khi tạo: {temp_filepath}")
            
    except Exception as e:
        logger.error(f"Lỗi khi tạo ảnh: {str(e)}")
        # Đảm bảo xóa file nếu có lỗi
        if temp_filepath and os.path.exists(temp_filepath):
            try:
                os.remove(temp_filepath)
            except:
                pass
        raise Exception(f"Lỗi khi tạo ảnh: {str(e)}")
    finally:
        # Xóa file HTML tạm
        if temp_html_path and os.path.exists(temp_html_path):
            try:
                os.remove(temp_html_path)
            except:
                pass

