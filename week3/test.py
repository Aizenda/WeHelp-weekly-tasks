from selenium import webdriver
from selenium.webdriver.common.by import By
import time,requests
from bs4 import BeautifulSoup
url = 'https://udn.com/news/cate/2/7227'
browser = webdriver.Chrome()
browser.get(url)
page = 5
for i in range(page):
    more = browser.find_element(By.CLASS_NAME,'btn.btn-ripple.btn-more.btn-more--news')
    more.click()
    time.sleep(2)
soup = BeautifulSoup(browser.page_source, 'html.parser')
soup2 = soup.find('section', {'class':'thumb-news more-news thumb-news--big context-box'})
divs = soup2.find_all('div', {'class':'story-list__news'})
for j in divs:
    title = j.find('div', {'class':'story-list__text'}).a.text.strip()
    time = j.find('time',"story-list__time").text.strip()
    print(title,time)
browser.quit()