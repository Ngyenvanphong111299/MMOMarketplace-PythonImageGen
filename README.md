# Image Generator API

API để tạo ảnh từ HTML với background từ Pexels.

## Cấu trúc dự án

```
python-imageGen/
├── app.py                 # FastAPI application (entry point)
├── config.py              # Configuration (API keys, constants)
├── models/                # Pydantic models
│   ├── __init__.py
│   └── request.py         # ImageRequest model
├── services/              # Business logic services
│   ├── __init__.py
│   ├── pexels_service.py  # Lấy ảnh từ Pexels API
│   ├── logo_service.py    # Xử lý logo (download, convert base64)
│   ├── html_service.py    # Tạo HTML content
│   └── image_service.py   # Tạo ảnh từ HTML
├── test_api.py            # Test script
├── requirements.txt        # Dependencies
└── logo.png               # Logo mặc định
```

## Cài đặt

```bash
pip install -r requirements.txt
```

## Chạy server

```bash
uvicorn app:app --reload
```

Server sẽ chạy tại: `http://localhost:8000`

## API Endpoints

### POST /generate-image

Tạo ảnh từ HTML với background từ Pexels.

**Request Body:**
```json
{
  "category_name": "AI INSIGN",
  "category_bg_color": "#00D4FF",
  "category_text_color": "#FFFFFF",
  "content": "<h1>Nội dung HTML</h1>",
  "background_theme": "technology",
  "logo_url": "https://example.com/logo.png",  // optional
  "show_logo": true  // optional, default: true
}
```

**Response:**
- Content-Type: `image/png`
- Body: Binary image data

### GET /

Thông tin API

### GET /health

Health check endpoint

### GET /docs

Swagger UI documentation

## Chạy test

```bash
python test_api.py
```

## Modules

### models/
- **request.py**: Pydantic model cho API request

### services/
- **pexels_service.py**: Service để lấy ảnh từ Pexels API
- **logo_service.py**: Service xử lý logo (download từ URL hoặc đọc local)
- **html_service.py**: Service tạo HTML template với các tham số
- **image_service.py**: Service tạo ảnh PNG từ HTML

### config.py
- Cấu hình API keys, constants, default values

## Tham số

- `category_name`: Tên danh mục hiển thị trên badge
- `category_bg_color`: Màu nền của badge (CSS color)
- `category_text_color`: Màu chữ của badge (CSS color)
- `content`: Nội dung HTML để hiển thị
- `background_theme`: Từ khóa để tìm ảnh từ Pexels
- `logo_url`: URL logo (optional, mặc định dùng logo.png)
- `show_logo`: Hiển thị logo hay không (optional, default: true)

## Tính năng

- ✅ Random vị trí text (left/center/right)
- ✅ Tự động lấy ảnh từ Pexels dựa trên theme
- ✅ Hỗ trợ logo từ URL hoặc file local
- ✅ Tùy chọn ẩn/hiện logo
- ✅ Custom màu sắc cho category badge
- ✅ HTML content tùy chỉnh

