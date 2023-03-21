import boto3
from botocore.exceptions import ClientError
from pprint import pprint
from boto3.dynamodb.conditions import Key, Attr
import marino
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import datetime
import telegramCustomFunc as teleFunc
import platform
import asyncio

try:
    roofCheck = 0
    # 사용자 컴퓨터 OS 확인 후 설정값 반환
    systemOS = platform.system()
    pathChromedriver = ''

    if systemOS == "Darwin":
        # pathChromedriver = '/Users/WMHY/Downloads/chromedriver'
        pathChromedriver = '/Users/home/coding/chromedriver' 
        # 맥북에서 테스트 할 때 사용
    elif systemOS == "Linux":
        pathChromedriver = './chromedriver'

    webdriver_options = webdriver.ChromeOptions()
    webdriver_options.add_argument('--headless')
    webdriver_options.add_argument('lang=ko_KR')
    webdriver_options.add_argument('window-size=1920x1080')
    webdriver_options.add_argument('disable-gpu')
    webdriver_options.add_argument('--incognito')
    webdriver_options.add_argument('--no-sandbox')
    webdriver_options.add_argument('--disable-setuid-sandbox')
    webdriver_options.add_argument('--disable-dev-shm-usage')



    webdriver_options.add_argument(
        'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36')

    # driver = webdriver.Chrome(pathChromedriver, options=webdriver_options)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=webdriver_options)

    def dbScan(campName, dynamodb=None):
        try:
            response = table.scan(
                FilterExpression = Attr('campName').eq(campName)
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            return response['Items']

    def dateExtract(data):
        date = []
        for i in range(0, len(data)):
            element = data[i]
            if element.get('selectedDate') != None:
                for j in range(0,len(element['selectedDate'])):
                    b = element['selectedDate'][j]['startDate']
                    if b not in date:
                        date.append(b)
        return date

    def listSearch(db):
        group = []
        for a in db:
            dateT = []
            if a.get('selectedDate'):
                for i in range(0,len(a['selectedDate'])):
                    dateT.append(a['selectedDate'][i]['startDate'])
                group.append({'id':a['chat_id'],'date':dateT})
        return sorted(group, key = lambda item: item['id'])

    def changeDateType(date):
        startDateYear = date[0:2]
        startDateMonth = date[2:4]
        startDateDay = date[4:]
        modDate = '20'+startDateYear+'-'+startDateMonth+'-'+startDateDay
        dateType = datetime.date(
        int('20'+startDateYear), int(startDateMonth), int(startDateDay))
        return {'modDate': modDate, 'dateType':dateType, 'startDateYear': startDateYear, 'startDateMonth': startDateMonth, 'startDateDay': startDateDay}


    while roofCheck < 1:
        try:
            # 오늘 날짜 확인
            today = datetime.date.today()
            startTime = time.time()

            campName = ['마리노캠핑장']
            marinoDate = []
            marinoTerm = []
            marinoChatId = []
            marinoList = []

            session = boto3.session.Session(profile_name='marinoCamp')

            dynamodb = session.resource('dynamodb')  # bucket 목록
            table = dynamodb.Table('campInfo')

            
            if __name__ == '__main__':
                marinoDb = sorted(dbScan('마리노캠핑장'), key=lambda item:item['chat_id'])
                marinoDate = dateExtract(marinoDb)
                marinoList = listSearch(marinoDb)

            # 마리노캠핑장 검색
            for index in range(len(marinoList)):
                dateList = marinoList[index]['date']
                mainID = marinoList[index]['id']
                for date in dateList:
                    searchDate = changeDateType(date)
                    if (today <= searchDate['dateType']):
                        marino.marinoSiteSearch(driver, mainID, searchDate)

            # endTime = time.time()
            # measureTime = endTime - startTime

            # 시간 측정
            # print("시간")
            # print(measureTime)
        except Exception as e:
            asyncio.run(teleFunc.telegramSimpleMessage('1003456250', '프로그램 오류'))
            print(datetime.datetime.now(),"===================================")
            print(e)
            time.sleep(300)
            pass

except Exception as e:
    print(datetime.datetime.now(),"===================================")
    print(e)
    asyncio.run(teleFunc.telegramSimpleMessage('1003456250', '프로그램 정지'))