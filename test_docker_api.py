"""
Script để test Image Generator API từ Docker container
"""
import requests
import json

API_URL = "http://localhost:8001"
API_KEY = "XzEcSl7aaW7wfeyxW74IGpGDBcM4noaO"

def test_root():
    """Test root endpoint"""
    print("\n" + "=" * 50)
    print("Test 1: Root endpoint")
    print("=" * 50)
    response = requests.get(f"{API_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_health():
    """Test health endpoint"""
    print("\n" + "=" * 50)
    print("Test 2: Health endpoint")
    print("=" * 50)
    response = requests.get(f"{API_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_generate_image_without_api_key():
    """Test generate image without API key (should fail)"""
    print("\n" + "=" * 50)
    print("Test 3: Generate image WITHOUT API key (should fail)")
    print("=" * 50)
    payload = {
        "category_name": "AI INSIGN",
        "category_bg_color": "#00D4FF",
        "category_text_color": "#FFFFFF",
        "content": "<h1>TEST IMAGE</h1>",
        "background_theme": "technology",
        "show_logo": False
    }
    try:
        response = requests.post(f"{API_URL}/generate-image", json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 401
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_generate_image_with_wrong_api_key():
    """Test generate image with wrong API key (should fail)"""
    print("\n" + "=" * 50)
    print("Test 4: Generate image WITH WRONG API key (should fail)")
    print("=" * 50)
    payload = {
        "category_name": "AI INSIGN",
        "category_bg_color": "#00D4FF",
        "category_text_color": "#FFFFFF",
        "content": "<h1>TEST IMAGE</h1>",
        "background_theme": "technology",
        "show_logo": False
    }
    headers = {"X-API-Key": "wrong-key"}
    try:
        response = requests.post(f"{API_URL}/generate-image", json=payload, headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 401
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_generate_image_with_correct_api_key():
    """Test generate image with correct API key"""
    print("\n" + "=" * 50)
    print("Test 5: Generate image WITH CORRECT API key")
    print("=" * 50)
    payload = {
        "category_name": "AI INSIGN",
        "category_bg_color": "#00D4FF",
        "category_text_color": "#FFFFFF",
        "content": "<h1>TEST IMAGE FROM DOCKER</h1>",
        "background_theme": "technology",
        "show_logo": False
    }
    headers = {"X-API-Key": API_KEY}
    try:
        response = requests.post(f"{API_URL}/generate-image", json=payload, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            # Lưu ảnh
            with open("test_docker_output.png", "wb") as f:
                f.write(response.content)
            print(f"✅ Image saved to test_docker_output.png")
            print(f"Image size: {len(response.content)} bytes")
            return True
        else:
            print(f"Response: {response.json()}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Chạy tất cả tests"""
    print("=" * 50)
    print("Testing Image Generator API from Docker")
    print("=" * 50)
    
    results = []
    results.append(("Root endpoint", test_root()))
    results.append(("Health endpoint", test_health()))
    results.append(("Without API key", test_generate_image_without_api_key()))
    results.append(("Wrong API key", test_generate_image_with_wrong_api_key()))
    results.append(("Correct API key", test_generate_image_with_correct_api_key()))
    
    print("\n" + "=" * 50)
    print("Test Results Summary")
    print("=" * 50)
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name}: {status}")
    
    all_passed = all(result for _, result in results)
    print("\n" + "=" * 50)
    if all_passed:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")
    print("=" * 50)

if __name__ == "__main__":
    main()

