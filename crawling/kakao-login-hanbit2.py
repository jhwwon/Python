from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# from bs4 import BeautifulSoup
import pyperclip
import time

# 크롬 옵션 (헤드리스로 돌리고 싶으면 주석 해제)
chrome_options = Options()
# chrome_options.add_argument("--headless=new")        # 브라우저를 띄우지 않고 실행
chrome_options.add_argument("--window-size=1280,900")  # 브라우저를 띄우고 실행
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=chrome_options)
                          
def clipboard_input(self, user_xpath, user_input):
    pyperclip.copy(user_input) # input을 클립보드로 복사
    driver.find_element(user_xpath).click() # element focus 설정
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform() # ctrl + v 전달

driver.get("https://accounts.kakao.com/login/?continue=https%3A%2F%2Fkauth.kakao.com%2Foauth%2Fauthorize%3Fclient_id%3Da2fa5be83aaa55cf7dbd01519af7b319%26redirect_uri%3Dhttps%253A%252F%252Fwww.hanbit.co.kr%252Flogin%252Fkakao%26response_type%3Dcode%26through_account%3Dtrue#login")
IDxPath='//*[@id="id_email_2"]'
PasswordxPath='//*[@id="id_password_3"]'

# input으로 따로 입력을 받을 예정이므로 미리 적지 않아도 됩니다
ID=input("카카오 아이디: ")
Password=input("카카오 비밀번호: ")

clipboard_input(driver, IDxPath, ID)
clipboard_input(driver,PasswordxPath,Password)
driver.find_element_by_xpath('//*[@id="login-form"]/fieldset/div[8]/button[1]').click()

time.sleep(5)
driver.get("https://www.hanbit.co.kr/myhanbit/myhanbit.html")