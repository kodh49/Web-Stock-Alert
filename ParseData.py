import requests
import pandas as pd
from bs4 import BeautifulSoup
import Preprocess


def getStockData(StockName, option):
    # automate this process : repeat checking all the stocks for every 5 seconds etc.
    finance_result = requests.get(
        'https://finance.naver.com/item/main.nhn?code='+Preprocess.getCode(StockName), headers={'User-Agent': 'Mozilla/5.0 (X11; Linux ppc64le; rv:75.0) Gecko/20100101 Firefox/75.0'})
    print(finance_result.content)
    finance_soup = BeautifulSoup(finance_result.text, "html.parser")
    finance_chart = finance_soup.find("div", {"id": "chart_area"})
    finance_rateInfo = finance_chart.find("div", {"class": "rate_info"})
    finance_exday = finance_rateInfo.find("p", {"class": "no_exday"})
    finance_today = finance_rateInfo.find("p", {"class": "no_today"})
    finance_value = finance_today.find("span", {"class": "blind"})
    finance_em = finance_exday.findAll('em')[1]
    finance_change = finance_em.findAll('span')
    finance_change = finance_change[:2]
    if option == "change":
        ChangeLists = []
        change = 0.0
        for tags in finance_change:
            ChangeLists.append(tags.string)
        if (len(ChangeLists) == 2):  # ex) ['+', '0.96'] or ['-', '0.72']
            if (ChangeLists[0] == '-'):
                change = -1*float(ChangeLists[1])
            else:  # ex) [0.00]
                change = float(ChangeLists[1])
        else:
            change = 0.0
        return change  # Sample Result : 0.28, -2.37, 0.00
    elif option == "value":
        value = finance_value.string
        return value


# 테스트용 데이터

# List = ["DSR", "GS글로벌", "HDC현대산업개발", "LG전자", "디피씨", "네이버", "메리츠증권", "명문제약", "모두투어리츠", "삼성SDI","삼성엔지니어링", "삼성출판사", "삼성화재해상보험", "삼영화학공업", "대한약품", "디엔에이링크", "셀트리온제약", "스튜디오산타클로스"]

List = ["NAVER"]

for item in List:
    print(item+"\t"+str(getStockData(item, "change")) +
          "%\t"+str(getStockData(item, "value")))
