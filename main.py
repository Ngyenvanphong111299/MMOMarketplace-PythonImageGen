"""
FastAPI application - Image Generator API
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from models.request import ImageRequest
from services.html_service import generate_html
from services.image_service import generate_image_from_html

# Import security modules
from app.middleware.rate_limit import RateLimitMiddleware
from app.middleware.security_headers import SecurityHeadersMiddleware
from app.security.dependencies import verify_api_key_header
from app.config import settings

app = FastAPI(
    title="Image Generator API",
    description="API để tạo ảnh từ HTML với background từ Pexels",
    version="1.0.0"
)

# Thêm CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.ALLOWED_METHODS,
    allow_headers=settings.ALLOWED_HEADERS,
)

# Thêm Security Headers middleware
app.add_middleware(SecurityHeadersMiddleware)

# Thêm Rate Limiting middleware
app.add_middleware(RateLimitMiddleware)


@app.post("/generate-image")
async def generate_image(
    request: ImageRequest,
    api_key_verified: bool = Depends(verify_api_key_header)
):
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
        api_key_verified: Xác thực API key (tự động từ dependency)
            
    Returns:
        Response: Ảnh PNG dạng binary
        
    Raises:
        HTTPException: Nếu có lỗi khi tạo ảnh hoặc API key không hợp lệ
        
    Yêu cầu: API key trong header X-API-Key
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

