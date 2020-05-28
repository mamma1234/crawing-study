# selenium01.py
from selenium import webdriver

# path = 'chormedriver.exe의 경로'
# path = 'C:/Work/chromedriver.exe'
path = 'C:\\github\\chromedriver.exe'

driver = webdriver.Chrome(path)
driver.get('http://www.google.com')

# q=blockchain 을 입력하고 검색하는 명령
search_keyword = driver.find_element_by_name('q')
search_keyword.send_keys('blockchain')
search_keyword.submit()


# from selenium import webdriver
# browser = webdriver.Chrome("C:\\github\\chromedriver.exe")
# browser.get(http://asdfkakd.com)
# browser.quit()