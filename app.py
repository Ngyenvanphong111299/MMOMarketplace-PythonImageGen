"""
FastAPI application - Image Generator API
"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from models.request import ImageRequest
from services.html_service import generate_html
from services.image_service import generate_image_from_html

app = FastAPI(
    title="Image Generator API",
    description="API để tạo ảnh từ HTML với background từ Pexels",
    version="1.0.0"
)


@app.post("/generate-image")
async def generate_image(request: ImageRequest):
    """
    Endpoint để tạo ảnh từ HTML với background từ Pexels
    
    Args:
        request: ImageRequest chứa các tham số:
            - category_name: Tên danh mục
            - category_bg_color: Màu nền danh mục
            - category_text_color: Màu chữ danh mục
            - content: Nội dung HTML
            - background_theme: Chủ đề để tìm ảnh từ Pexels
            - logo_url: URL logo (optional)
            - show_logo: Hiển thị logo hay không (optional)
            
    Returns:
        Response: Ảnh PNG dạng binary
        
    Raises:
        HTTPException: Nếu có lỗi khi tạo ảnh
    """
    try:
        # Tạo HTML content
        html_content = generate_html(
            category_name=request.category_name,
            category_bg_color=request.category_bg_color,
            category_text_color=request.category_text_color,
            content=request.content,
            background_theme=request.background_theme,
            logo_url=request.logo_url,
            show_logo=request.show_logo
        )
        
        # Tạo ảnh từ HTML
        image_data = generate_image_from_html(html_content)
        
        return Response(content=image_data, media_type="image/png")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi tạo ảnh: {str(e)}")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Image Generator API",
        "version": "1.0.0",
        "endpoint": "/generate-image",
        "method": "POST",
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}
