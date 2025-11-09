"""
Script để tạo file HTML test
"""
from services.html_service import generate_html

# Tạo HTML với cùng tham số như test
html_content = generate_html(
    category_name="AI INSIGN",
    category_bg_color="#00D4FF",
    category_text_color="#FFFFFF",
    content="<h1><span class='highlight' data-text='CHATGPT'>CHATGPT</span> DA THAY DOI MOI THU</h1>",
    background_theme="technology",
    logo_url=None,
    show_logo=True
)

# Lưu vào file
with open("test.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("OK! Da tao file test.html")
print("Ban co the mo file nay trong browser de xem")

