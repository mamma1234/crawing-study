# selenium01.py
from selenium import webdriver

# path = 'chormedriver.exe의 경로'
# path = 'C:/Work/chromedriver.exe'
path = 'C:\\github\\chromedriver.exe'

driver = webdriver.Chrome(path)

driver.implicitly_wait(3)

driver.get("http://mainia.tistory.com/admin/center/")


login = driver.find_element_by_id("loginId")

login.send_keys("gonhaha201@gmail.com")

login = driver.find_element_by_id("loginPw")

login.send_keys("****")

driver.find_element_by_xpath("""//*[@id="authForm"]/fieldset/div/button""").click()
