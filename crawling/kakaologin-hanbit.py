from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

# 크롬 옵션 (헤드리스로 돌리고 싶으면 주석 해제)
chrome_options = Options()
# chrome_options.add_argument("--headless=new")        # 브라우저를 띄우지 않고 실행
chrome_options.add_argument("--window-size=1280,900")  # 브라우저를 띄우고 실행

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=chrome_options)

try:
  driver.get("https://www.hanbit.co.kr/login")  # 한빛+로 이동
  wait = WebDriverWait(driver, 15)   # 최대 15초 대기

  # 카카오 로그인 버튼 찾기
  kakao_login_btn_selector = (By.CSS_SELECTOR, "body > div.flex.min-h-screen.flex-col.items-center.justify-center.bg-slate-50.p-4.sm\:p-6.md\:p-8 > div.w-full.max-w-\[480px\].rounded-2xl.bg-white\/80.backdrop-blur-sm.px-6.py-6.sm\:px-8.shadow-lg.ring-1.ring-gray-100\/50.transition-all.duration-300 > button")
  # 카카오 로그인 버튼이 나타날 때까지 대기
  kakao_login_btn = wait.until(EC.element_to_be_clickable(kakao_login_btn_selector))
  # 카카오 로그인 버튼 클릭
  kakao_login_btn.click()
  print("카카오 로그인 버튼 클릭 완료")

  # 새 창으로 팝업이 나올 시 전환
  driver.switch_to.window(driver.window_handles[-1])  

  # 카카오 로그인 아이디 입력창을 찾기
  kakaoid_selector = (By.CSS_SELECTOR, "input#loginId--1")
  kakaoid_input = wait.until(EC.presence_of_element_located(kakaoid_selector)) 
  # 카카오 로그인 패스워드 입력창을 찾기
  kakaopw_selector = (By.CSS_SELECTOR, "input#password--2")
  kakaopw_input = wait.until(EC.presence_of_element_located(kakaopw_selector)) 

  # 카카오 아이디와 패스워드 입력하기
  kakaoid_input.send_keys("내 아이디")    # 자신의 카카오 아이디로 변경
  kakaopw_input.send_keys("내 비밀번호")     # 자신의 카카오 패스워드로 변경
  
  # time.sleep(10)

  # 카카오 실제 로그인 버튼 찾기
  kakao_login_btn_selector = (By.CSS_SELECTOR, "#mainContent > div > div > form > div.confirm_btn > button.btn_g.highlight.submit")
  # 카카오 실제 로그인 버튼이 나타날 때까지 대기
  kakao_login_btn = wait.until(EC.element_to_be_clickable(kakao_login_btn_selector))
  # 카카오 실제 로그인 버튼 클릭
  kakao_login_btn.click()
  print("카카오 실제 로그인 버튼 클릭 완료")

  # 다시 원래 창으로 전환 
  driver.switch_to.window(driver.window_handles[0]) 
  
  # 저정한 데이터 파일을 브라우저 쿠키 저장소에 저장
  with open("hanbit_kakao_cookie.json", "r", encoding="utf-8") as f:
      print('cookie 통과')
      cookies = json.load(f)
      for cookie in cookies:
          print(cookie)
          try:
              if cookie["domain"] == '.www.hanbit.co.kr' or cookie["domain"] == '.hanbit.co.kr':
                  pass
              driver.add_cookie(cookie)  # 데이터 파일에 저장된 데이터를 쿠키에 저장
          except Exception as e:
              print('오류:', e)

  time.sleep(60)

  # 현재 로그인한 정보를 저장한 쿠키를 데이터 파일로 저장
  cookies = driver.get_cookies()
  with open("hanbit_kakao_cookie.json", "w", encoding="utf-8") as f:
      json.dump(cookies, f)
  print('카카오 쿠키 저장완료')

  driver.get("https://www.hanbit.co.kr/myhanbit/myhanbit.html")
  time.sleep(5)
except:
  pass
finally:
  driver.quit() # 브라우저 종료
