"""
Service để tạo ảnh từ HTML sử dụng Playwright
"""
import os
import uuid
import logging
import tempfile
import asyncio
from playwright.async_api import async_playwright
from PIL import Image

# Image dimensions
IMAGE_WIDTH = 1280
IMAGE_HEIGHT = 850

# Thiết lập logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def generate_image_from_html_async(html_content: str) -> bytes:
    """
    Tạo ảnh PNG từ HTML content sử dụng Playwright
    
    Args:
        html_content: HTML string
        
    Returns:
        bytes: Ảnh PNG dạng binary
        
    Raises:
        Exception: Nếu có lỗi khi tạo ảnh
    """
    temp_html_path = None
    temp_filepath = None
    
    try:
        # Tạo thư mục temp nếu chưa có
        temp_dir = os.path.join(os.getcwd(), "temp")
        os.makedirs(temp_dir, exist_ok=True)
        
        # Tạo file HTML tạm
        temp_filename = f"temp_{uuid.uuid4().hex}.html"
        temp_html_path = os.path.join(temp_dir, temp_filename)
        
        with open(temp_html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"Tạo ảnh từ HTML, HTML file: {temp_html_path}")
        
        # Tạo file ảnh tạm
        image_filename = f"temp_{uuid.uuid4().hex}.png"
        temp_filepath = os.path.join(temp_dir, image_filename)
        
        # Sử dụng Playwright async để tạo screenshot
        async with async_playwright() as p:
            # Khởi động browser với các options cần thiết cho Docker
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                    '--disable-software-rasterizer',
                    '--disable-extensions',
                ]
            )
            
            try:
                # Tạo context với viewport size
                context = await browser.new_context(
                    viewport={'width': IMAGE_WIDTH, 'height': IMAGE_HEIGHT},
                    device_scale_factor=1
                )
                
                # Tạo page
                page = await context.new_page()
                
                # Load HTML từ file
                # Sử dụng file:// protocol để load local file
                file_url = f"file://{temp_html_path}"
                await page.goto(file_url, wait_until='networkidle', timeout=30000)
                
                # Đợi một chút để đảm bảo render xong
                await page.wait_for_timeout(1000)
                
                # Tạo screenshot
                screenshot_bytes = await page.screenshot(
                    type='png',
                    full_page=False,
                    clip={'x': 0, 'y': 0, 'width': IMAGE_WIDTH, 'height': IMAGE_HEIGHT}
                )
                
                logger.info(f"Đã tạo screenshot thành công, size: {len(screenshot_bytes)} bytes")
                
                # Lưu vào file tạm để xử lý với Pillow
                with open(temp_filepath, 'wb') as f:
                    f.write(screenshot_bytes)
                
            finally:
                await browser.close()
        
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
        import traceback
        logger.error(traceback.format_exc())
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


# Giữ lại function sync để tương thích nếu cần
def generate_image_from_html(html_content: str) -> bytes:
    """
    Wrapper function để chạy async function trong sync context
    Chỉ dùng khi không có event loop đang chạy
    """
    return asyncio.run(generate_image_from_html_async(html_content))
