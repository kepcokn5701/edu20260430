import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
from io import BytesIO

html_path = os.path.abspath(r"c:\Users\Admin\Desktop\project\edu\클로드_실무활용_가이드.html")
pdf_path = r"c:\Users\Admin\Desktop\project\edu\클로드_실무활용_가이드.pdf"

# Chrome 설정 (16:9 비율)
opts = Options()
opts.add_argument('--headless=new')
opts.add_argument('--window-size=1920,1080')
opts.add_argument('--force-device-scale-factor=2')
opts.add_argument('--no-sandbox')
opts.add_argument('--disable-gpu')
opts.add_argument('--ignore-certificate-errors')

driver = webdriver.Chrome(options=opts)
driver.get(f'file:///{html_path}')
time.sleep(3)

# 네비게이션 바 숨기기
driver.execute_script("document.querySelector('.nav-bar').style.display = 'none';")
time.sleep(0.5)

total_slides = 7
screenshots = []

for i in range(total_slides):
    time.sleep(1)
    png = driver.get_screenshot_as_png()
    img = Image.open(BytesIO(png)).convert('RGB')
    screenshots.append(img)
    print(f"  슬라이드 {i+1}/{total_slides} 캡처 완료")

    if i < total_slides - 1:
        driver.execute_script("changeSlide(1);")

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
