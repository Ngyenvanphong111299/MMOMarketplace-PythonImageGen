"""
Service để lấy ảnh từ Pexels API
"""
import requests
import random

# Hardcode Pexels API key
PEXELS_API_KEY = "EY2W2pV8aA0CN0sJOrPfKOl6osKlxnWnp9gdHo1HfwnaKuELZJHP7BNm"


def get_pexels_image(query: str = "ai technology"):
    """
    Lấy ảnh từ Pexels và trả về dict chứa:
    - url: URL ảnh
    - photographer: Tên tác giả
    - photographer_url: Link Pexels của tác giả
    - pexels_url: Link ảnh trên Pexels
    
    Args:
        query: Từ khóa tìm kiếm ảnh
        
    Returns:
        dict hoặc None nếu có lỗi
    """
    url = "https://api.pexels.com/v1/search"
    params = {
        "query": query,
        "orientation": "landscape",
        "per_page": 30
    }
    headers = {"Authorization": PEXELS_API_KEY}
    
    try:
        res = requests.get(url, params=params, headers=headers)
        
        if res.status_code == 401:
            print(f"Loi xac thuc: Kiem tra lai API Key")
            print(f"Response: {res.text[:200]}")
            return None
            
        res.raise_for_status()
        data = res.json()
        photos = data.get("photos", [])
        
        if not photos:
            print("Khong tim thay anh nao")
            return None
        
        # Chọn ảnh ngẫu nhiên từ kết quả
        selected_photo = random.choice(photos)
        
        # Lấy thông tin cần thiết
        image_info = {
            "url": selected_photo["src"]["large"],
            "photographer": selected_photo["photographer"],
            "photographer_url": selected_photo["photographer_url"],
            "pexels_url": selected_photo["url"]
        }
        
        return image_info
        
    except requests.exceptions.HTTPError as e:
        print(f"Loi HTTP khi lay anh tu Pexels: {e}")
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text[:200]}")
        return None
    except Exception as e:
        print(f"Loi khi lay anh tu Pexels: {e}")
        return None

