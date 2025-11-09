"""
Script để test Image Generator API
"""
import requests
import json
import sys
import codecs

# Fix encoding cho Windows console
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

API_URL = "http://localhost:8000/generate-image"

def test_basic_request():
    """Test request cơ bản với logo"""
    print("\n" + "=" * 50)
    print("Test 1: Request co ban (co logo)")
    print("=" * 50)
    payload = {
        "category_name": "AI INSIGN",
        "category_bg_color": "#00D4FF",
        "category_text_color": "#FFFFFF",
        "content": "<h1><span class='highlight' data-text='CHATGPT'>CHATGPT</span> DA THAY DOI MOI THU</h1>",
        "background_theme": "technology",
        "show_logo": True
    }
    return _send_request_and_save(payload, "test_output_basic.png")


def test_with_logo_url():
    """Test với logo URL tùy chỉnh"""
    print("\n" + "=" * 50)
    print("Test 2: Request voi logo URL")
    print("=" * 50)
    payload = {
        "category_name": "AI INSIGN",
        "category_bg_color": "#00D4FF",
        "category_text_color": "#FFFFFF",
        "content": "<h1><span class='highlight' data-text='CHATGPT'>CHATGPT</span> DA THAY DOI MOI THU</h1>",
        "background_theme": "technology",
        "logo_url": "https://via.placeholder.com/200",
        "show_logo": True
    }
    return _send_request_and_save(payload, "test_output_logo_url.png")


def test_no_logo():
    """Test ẩn logo"""
    print("\n" + "=" * 50)
    print("Test 3: Request an logo")
    print("=" * 50)
    payload = {
        "category_name": "AI INSIGN",
        "category_bg_color": "#00D4FF",
        "category_text_color": "#FFFFFF",
        "content": "<h1><span class='highlight' data-text='CHATGPT'>CHATGPT</span> DA THAY DOI MOI THU</h1>",
        "background_theme": "technology",
        "show_logo": False
    }
    return _send_request_and_save(payload, "test_output_no_logo.png")


def test_different_colors():
    """Test với màu sắc khác nhau"""
    print("\n" + "=" * 50)
    print("Test 4: Request voi mau sac khac nhau")
    print("=" * 50)
    payload = {
        "category_name": "TECH NEWS",
        "category_bg_color": "#FF6B6B",
        "category_text_color": "#FFFFFF",
        "content": "<h1>CONG NGHE MOI NHAT</h1><h2>Cap nhat hang ngay</h2>",
        "background_theme": "technology",
        "show_logo": True
    }
    return _send_request_and_save(payload, "test_output_colors.png")


def test_html_content():
    """Test với HTML content phức tạp"""
    print("\n" + "=" * 50)
    print("Test 5: Request voi HTML content phuc tap")
    print("=" * 50)
    payload = {
        "category_name": "BLOG POST",
        "category_bg_color": "#9B59B6",
        "category_text_color": "#FFFFFF",
        "content": "<h1>Bai viet hay</h1><h2>Phu de quan trong</h2><p>Noi dung bai viet voi <strong>chu dam</strong> va <em>chu nghieng</em></p>",
        "background_theme": "technology",
        "show_logo": True
    }
    return _send_request_and_save(payload, "test_output_html.png")


def _send_request_and_save(payload, output_file):
    """Gửi request và lưu ảnh"""
    try:
        response = requests.post(API_URL, json=payload, timeout=30)
        response.raise_for_status()
        
        with open(output_file, "wb") as f:
            f.write(response.content)
        
        file_size = len(response.content)
        print(f"OK! Da luu anh vao {output_file}")
        print(f"  Kich thuoc: {file_size} bytes")
        return True
    except requests.exceptions.RequestException as e:
        print(f"LOI: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"  Response: {e.response.text[:200]}")
        return False
    except Exception as e:
        print(f"LOI: {e}")
        return False


def main():
    """Chạy tất cả các test"""
    print("=" * 50)
    print("BAT DAU TEST API")
    print("=" * 50)
    print(f"API URL: {API_URL}")
    print("\nLuu y: Dam bao server dang chay (uvicorn app:app --reload)")
    print("=" * 50)
    
    # Kiểm tra server có đang chạy không
    try:
        health_response = requests.get("http://localhost:8000/health", timeout=5)
        if health_response.status_code == 200:
            print("OK! Server dang chay\n")
        else:
            print("WARNING: Server tra ve status code khac 200\n")
    except Exception as e:
        print(f"LOI: Khong the ket noi den server: {e}")
        print("Vui long khoi dong server bang: uvicorn app:app --reload")
        return
    
    # Chạy các test
    results = []
    results.append(("Test co ban", test_basic_request()))
    results.append(("Test voi logo URL", test_with_logo_url()))
    results.append(("Test an logo", test_no_logo()))
    results.append(("Test mau sac", test_different_colors()))
    results.append(("Test HTML content", test_html_content()))
    
    # Tổng kết
    print("\n" + "=" * 50)
    print("KET QUA TEST")
    print("=" * 50)
    passed = 0
    for name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{status} - {name}")
        if result:
            passed += 1
    
    print(f"\nTong ket: {passed}/{len(results)} test passed")
    print("=" * 50)


if __name__ == "__main__":
    main()

