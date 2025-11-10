#!/usr/bin/env python3
"""Test Html2Image trong Docker"""
from html2image import Html2Image
import os

hti = Html2Image()
hti.browser_executable = '/usr/local/bin/chromium-wrapper.sh'
hti.output_path = '/app/temp'
hti.size = (1280, 850)

print(f"Browser executable: {hti.browser_executable}")
print(f"Output path: {hti.output_path}")
print(f"Size: {hti.size}")

html_content = '<html><body><h1>Test</h1></body></html>'

try:
    result = hti.screenshot(
        html_str=html_content,
        save_as='test.png',
        size=(1280, 850)
    )
    print(f'Screenshot result: {result}')
    
    # Kiểm tra file
    temp_dir = '/app/temp'
    files = os.listdir(temp_dir)
    print(f'Files in {temp_dir}: {files}')
    
    test_file = os.path.join(temp_dir, 'test.png')
    if os.path.exists(test_file):
        print(f'File exists: {test_file}')
        print(f'File size: {os.path.getsize(test_file)} bytes')
    else:
        print(f'File does not exist: {test_file}')
        
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()

