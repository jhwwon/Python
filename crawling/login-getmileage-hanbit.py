from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# 크롬 옵션 (헤드리스로 돌리고 싶으면 주석 해제)
chrome_options = Options()
# chrome_options.add_argument("--headless=new")        # 브라우저를 띄우지 않고 실행
chrome_options.add_argument("--window-size=1280,900")  # 브라우저를 띄우고 실행

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=chrome_options)

try:
  driver.get("https://www.hanbit.co.kr/login?redirect=https%3A%2F%2Fwww.hanbit.co.kr%2Findex.html")  # 한빛+로 이동

  wait = WebDriverWait(driver, 15)   # 최대 15초 대기

  # 아이디 입력창을 찾기
  id_selector = (By.CSS_SELECTOR, "input[name='id']")
  # selector 요소가 나타날 때까지 대기
  id_input = wait.until(EC.presence_of_element_located(id_selector))  
  
  # 패스워드 입력창을 찾기
  pw_selector = (By.CSS_SELECTOR, "input[name='password']")
  # selector 요소가 나타날 때까지 대기
  pw_input = wait.until(EC.presence_of_element_located(pw_selector))  

  # 아이디와 패스워드 입력하기
  id_input.send_keys("")    # 자신의 아이디로 변경
  pw_input.send_keys("")      # 자신의 패스워드로 변경

  # time.sleep(10)  # 10초 대기
  # print("아이디와 패스워드 입력 완료")

  # 로그인 버튼 찾기
  login_btn_selector = (By.CSS_SELECTOR, "button[type='submit']")
  # 로그인 버튼이 나타날 때까지 대기
  login_btn = wait.until(EC.element_to_be_clickable(login_btn_selector))
  # 로그인 버튼 클릭하기
  login_btn.click()
  print("로그인 버튼 클릭 완료")

  # 5초 대기(로그인 처리하는데 시간이 걸릴 수 있음)
  time.sleep(5)  

  # 마이페이지로 이동
  driver.get("https://www.hanbit.co.kr/myhanbit/myhanbit.html")  
  # 10초 대기
  # time.sleep(10)

  # 마일리지와 이코인 tag 가져오기
  mileage_selector = (By.CSS_SELECTOR, "#container > div > div.sm_mymileage > dl.mileage_section1 > dd > span") # 마일리지 셀렉터 입력
  e_coin = (By.CSS_SELECTOR, "#container > div > div.sm_mymileage > dl.mileage_section2 > dd > span") # 이코인 셀렉터 입력

  # 마일리지와 요소가 나타날 때까지 대기
  mileage = wait.until(EC.presence_of_element_located(mileage_selector))
  # 이코인 요소가 나타날 때까지 대기
  ecoin = wait.until(EC.presence_of_element_located(e_coin))

  print("마일리지: " + mileage.text)
  print("이코인: " + ecoin.text)
except:
  pass
finally:
  driver.quit() # 브라우저 종료