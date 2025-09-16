from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time

# 예약 우선 순위 시간 목록 (빠른 시간부터 우선)
target_times = [
    "오전 10:30"
]

# 예약 페이지 URL
url = "https://booking.naver.com/booking/12/bizes/1437383/items/6839220"

# Chrome 설정
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)
driver.get(url)

# 수동 로그인 대기
input("🔐 로그인 후 시간 선택 화면에서 Enter를 누르세요...")

refresh_count = 0

def try_reservation():
    global refresh_count
    wait = WebDriverWait(driver, 5)

    try:
        time_buttons = driver.find_elements(By.CLASS_NAME, "btn_time")

        for btn in time_buttons:
            class_name = btn.get_attribute("class")
            btn_text = btn.text.strip().replace('\n', ' ')
            print(f"🕒 버튼: {btn_text} | 클래스: {class_name}")

            if "unselectable" in class_name:
                continue  # 매진된 시간

            for time_label in target_times:
                if time_label in btn_text:
                    print(f"✅ 예약 시도: {time_label}")
                    btn.click()

                    # '다음' 버튼 클릭
                    next_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "다음")]')))
                    next_button.click()

                    # '동의하고 예매하기' 버튼 클릭
                    confirm_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "동의하고 예매하기")]')))
                    confirm_button.click()

                    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(f"🎉 예매 성공: {time_label}")
                    print(f"📅 완료 시각: {now}")
                    print(f"🔄 총 새로고침 횟수: {refresh_count}")
                    return True

    except Exception as e:
        print(f"⚠️ 예외 발생 (무시): {e}")

    return False

# 새로고침 감시 루프
while True:
    refresh_count += 1
    print(f"\n🔄 새로고침 #{refresh_count}")
    
    driver.refresh()
    time.sleep(1)  # DOM 뜨는 시간

    if try_reservation():
        break

    time.sleep(0.5)  # 🔁 새로고침 간격

