import requests
import pandas as pd
from bs4 import BeautifulSoup
import Preprocess
import ParseData
import schedule
import threading
from datetime import datetime


def ifStockExceeds(StockName, maximum, minimum):  # maximum > 0, minimum > 0
    currentVal = ParseData.getStockData(StockName, "value")  # Get 현재 시가
    currentChange = ParseData.getStockData(StockName, "change")
    currentTime = datetime.now().time()
    output = []
    if currentChange >= maximum:  # 주가의 상승폭이 알림 설정한 값보다 같거나 높으면
        output.append(currentTime)
        output.append(StockName)
        output.append(Preprocess.getCode(StockName))
        output.append(currentChange)
        output.append(currentVal)
        return output
    elif currentChange <= (-1*minimum):  # 주가의 상승폭이 알림 설정한 값보다 같거나 떨어지면
        output.append(currentTime)
        output.append(StockName)
        output.append(Preprocess.getCode(StockName))
        output.append(currentChange)
        output.append(currentVal)
        return output
    else:  # 등락폭이 작아서 알림을 내보낼 필요가 없을 때
        return 0
        # 출력에 사용될 데이터들
        # Current Time : 00시 00분 00초 00
        # StockName : 삼성전자 << 그대로 호출
        # Stock Code : 000000
        # + 부호와 0.00 실제 변화량
        # 현재 시가 : 84000


# ex) StockList = ["삼성전자", "메리츠화재", "이화전기"]
def moniterStock(StockList, maximum, minimum):
    MessageData = []
    for StockName in StockList:  # 만약 3개 모두 알림 설정 조건을 충족하는 경우
        if (ifStockExceeds(StockName, maximum, minimum) != 0):
            MessageData.append(ifStockExceeds(StockName, maximum, minimum))
    return MessageData  # [[삼성전자 관련 데이터], [메리츠화재 관련 데이터], [이화전기 관련 데이터]]

# 실제로는 사용자가 제공한 리스트가 될 것
# print(moniterStock(SampleStockList, 3, 3))
