import os
import time
import json
import base64
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from PIL import Image
from io import BytesIO

html_path = os.path.abspath(r"c:\Users\Admin\Desktop\project\edu\클로드_실전마스터_슬라이드쇼.html")
pdf_path = r"c:\Users\Admin\Desktop\project\edu\클로드_실전마스터_슬라이드쇼.pdf"

# Chrome 설정
opts = Options()
opts.add_argument('--headless=new')
opts.add_argument('--window-size=1920,1080')
opts.add_argument('--force-device-scale-factor=2')
opts.add_argument('--no-sandbox')
opts.add_argument('--disable-gpu')
opts.add_argument('--ignore-certificate-errors')

driver = webdriver.Chrome(options=opts)
driver.get(f'file:///{html_path}')
time.sleep(3)  # React 렌더링 + 폰트 로딩 대기

total_slides = 5
screenshots = []

for i in range(total_slides):
    time.sleep(1)  # 애니메이션 완료 대기
    png = driver.get_screenshot_as_png()
    img = Image.open(BytesIO(png)).convert('RGB')
    screenshots.append(img)
    print(f"  슬라이드 {i+1}/{total_slides} 캡처 완료")

    # 다음 슬라이드로 이동 (마지막 제외)
    if i < total_slides - 1:
        driver.execute_script("""
            const btns = document.querySelectorAll('.nav-btn');
            btns[btns.length - 1].click();
        """)

driver.quit()

# PDF로 합치기
screenshots[0].save(
    pdf_path,
    save_all=True,
    append_images=screenshots[1:],
    resolution=150
)

print(f"\nPDF 생성 완료: {pdf_path}")
print(f"총 {total_slides}페이지")
