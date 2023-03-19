from bs4 import BeautifulSoup
import time
from telegramCustomFunc import telegramSendMessage
import datetime
from dateutil.relativedelta import relativedelta
import asyncio
from selenium.webdriver.common.by import By


today = datetime.date.today()
nextMonth = today + relativedelta(months=1)

def connectWebsite(driver):

    url = 'https://www.yeongdo.go.kr/marinocamping/00003/00015/00028.web'

    driver.get(url)
    time.sleep(0.3)

    xpath = "//*[@id='campNight1']"
    driver.find_element(By.XPATH, xpath).click()

    time.sleep(0.3)

def siteSearch(driver, chatId, date):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    activeSite = soup.find_all("button", {"title": "예약가능"})
    if activeSite:
        for dayText in activeSite:
            siteNum = dayText.get_text().strip()
            asyncio.run(telegramSendMessage(
                str(chatId), '마리노캠핑장', date['modDate'], siteNum,))

def nextMonthCheck(driver, month):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    active = soup.find("a", {"class": "b1 next btn-month"})
    if active["data-mm"] == month:  
        return True
    else:
        return False

def marinoSiteSearch(driver, chatId, date):
    connectWebsite(driver)

    if (nextMonthCheck(driver, date['startDateMonth'])):
        xpath = "//*[@id='calendar']/a[2]"
        driver.find_element(By.XPATH, xpath).click()
        time.sleep(0.3)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        active = soup.find_all("a", {"title": "예약가능"})
        for activeDay in active:
            dayText = activeDay.get_text().strip()
            if len(dayText) == 1:
                dayTextcheck = '0' + dayText
            if  dayTextcheck == date['startDateDay']:
                xpath = "//*[@id='date" + dayText + "']/a"
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(0.3)
                # 오토사이트 선택
                xpath = "//*[@id='siteGubun2']"
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(0.3)
                siteSearch(driver, chatId, date)
                # 일반사이트 선택
                xpath = "//*[@id='siteGubun3']"
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(0.3)
                siteSearch(driver, chatId, date)

    else:
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        active = soup.find_all("a", {"title": "예약가능"})
        for activeDay in active:
            dayText = activeDay.get_text().strip()
            if  dayText == date['startDateDay']:
                xpath = "//*[@id='date" + dayText + "']/a"
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(0.3)
                # 오토사이트 선택
                xpath = "//*[@id='siteGubun2']"
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(0.3)
                siteSearch(driver, chatId, date)
                # 일반사이트 선택
                xpath = "//*[@id='siteGubun3']"
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(0.3)
                siteSearch(driver, chatId, date)    