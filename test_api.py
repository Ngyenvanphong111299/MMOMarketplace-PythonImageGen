"""
Script test API để tao anh
"""
import requests
import json
import os
import sys

# Fix encoding cho Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# URL của API (mặc định localhost:8000)
API_URL = "http://localhost:8000/generate-image"

def test_basic_request():
    """Test với các tham số cơ bản"""
    print("=" * 50)
    print("Test 1: Request cơ bản")
    print("=" * 50)
    
    payload = {
        "category_name": "AI INSIGN",
        "category_bg_color": "linear-gradient(135deg, #00D4FF 0%, #00A8CC 50%, #0077BE 100%)",
        "category_text_color": "#FFFFFF",
        "content": "<span class='highlight' data-text='CHATGPT'>CHATGPT</span> ĐÃ THAY ĐỔI MỌI THỨ",
        "background_theme": "surprised man expression shocked face portrait"
    }
    
    try:
        response = requests.post(API_URL, json=payload, timeout=60)
        response.raise_for_status()
        
        # Lưu ảnh
        output_file = "test_output_basic.png"
        with open(output_file, "wb") as f:
            f.write(response.content)
        print(f"OK! Da luu anh vao {output_file}")
        print(f"  Kich thuoc: {len(response.content)} bytes")
        return True
    except Exception as e:
        print(f"LOI: {e}")
        return False

def test_with_logo_url():
    """Test với logo URL"""
    print("\n" + "=" * 50)
    print("Test 2: Request với logo URL")
    print("=" * 50)
    
    payload = {
        "category_name": "TECH NEWS",
        "category_bg_color": "#FF6B6B",
        "category_text_color": "#FFFFFF",
        "content": "CÔNG NGHỆ MỚI NHẤT 2024",
        "background_theme": "technology innovation",
        "logo_url": "https://via.placeholder.com/200/FF6B6B/FFFFFF?text=LOGO",
        "show_logo": True
    }
    
    try:
        response = requests.post(API_URL, json=payload, timeout=60)
        response.raise_for_status()
        
        output_file = "test_output_logo_url.png"
        with open(output_file, "wb") as f:
            f.write(response.content)
        print(f"OK! Da luu anh vao {output_file}")
        print(f"  Kich thuoc: {len(response.content)} bytes")
        return True
    except Exception as e:
        print(f"LOI: {e}")
        return False

def test_hide_logo():
    """Test ẩn logo"""
    print("\n" + "=" * 50)
    print("Test 3: Request ẩn logo")
    print("=" * 50)
    
    payload = {
        "category_name": "BUSINESS",
        "category_bg_color": "#4ECDC4",
        "category_text_color": "#FFFFFF",
        "content": "KHỞI NGHIỆP THÀNH CÔNG",
        "background_theme": "business success",
        "show_logo": False
    }
    
    try:
        response = requests.post(API_URL, json=payload, timeout=60)
        response.raise_for_status()
        
        output_file = "test_output_no_logo.png"
        with open(output_file, "wb") as f:
            f.write(response.content)
        print(f"OK! Da luu anh vao {output_file}")
        print(f"  Kich thuoc: {len(response.content)} bytes")
        return True
    except Exception as e:
        print(f"LOI: {e}")
        return False

def test_different_colors():
    """Test với các màu sắc khác nhau"""
    print("\n" + "=" * 50)
    print("Test 4: Request với màu sắc khác nhau")
    print("=" * 50)
    
    payload = {
        "category_name": "DESIGN",
        "category_bg_color": "#9B59B6",
        "category_text_color": "#FFFFFF",
        "content": "THIẾT KẾ SÁNG TẠO",
        "background_theme": "creative design art"
    }
    
    try:
        response = requests.post(API_URL, json=payload, timeout=60)
        response.raise_for_status()
        
        output_file = "test_output_colors.png"
        with open(output_file, "wb") as f:
            f.write(response.content)
        print(f"OK! Da luu anh vao {output_file}")
        print(f"  Kich thuoc: {len(response.content)} bytes")
        return True
    except Exception as e:
        print(f"LOI: {e}")
        return False

def test_html_content():
    """Test với nội dung HTML phức tạp"""
    print("\n" + "=" * 50)
    print("Test 5: Request với HTML content phức tạp")
    print("=" * 50)
    
    html_content = """
    <div>
        <h2 style="font-size: 60px; color: #FFD700;">TITLE 1</h2>
        <p style="font-size: 40px; color: #FFFFFF;">Subtitle here</p>
    </div>
    """
    
    payload = {
        "category_name": "CUSTOM HTML",
        "category_bg_color": "#E74C3C",
        "category_text_color": "#FFFFFF",
        "content": html_content,
        "background_theme": "abstract colorful"
    }
    
    try:
        response = requests.post(API_URL, json=payload, timeout=60)
        response.raise_for_status()
        
        output_file = "test_output_html.png"
        with open(output_file, "wb") as f:
            f.write(response.content)
        print(f"OK! Da luu anh vao {output_file}")
        print(f"  Kich thuoc: {len(response.content)} bytes")
        return True
    except Exception as e:
        print(f"LOI: {e}")
        return False

def main():
    """Chay tat ca cac test"""
    print("\n" + "=" * 50)
    print("BAT DAU TEST API")
    print("=" * 50)
    print(f"API URL: {API_URL}")
    print("\nLuu y: Dam bao server dang chay (uvicorn app:app --reload)")
    print("=" * 50)
    
    # Kiem tra server co dang chay khong
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        print("OK! Server dang chay\n")
    except:
        print("LOI! Khong the ket noi den server!")
        print("  Hay chay: uvicorn app:app --reload")
        return
    
    results = []
    results.append(("Test co ban", test_basic_request()))
    results.append(("Test voi logo URL", test_with_logo_url()))
    results.append(("Test an logo", test_hide_logo()))
    results.append(("Test mau sac", test_different_colors()))
    results.append(("Test HTML content", test_html_content()))
    
    # Tong ket
    print("\n" + "=" * 50)
    print("KET QUA TEST")
    print("=" * 50)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{status} - {name}")
    
    print(f"\nTong ket: {passed}/{total} test passed")
    print("=" * 50)

if __name__ == "__main__":
    main()

