import requests
import sys
import os
import time
import pickle
from datetime import datetime
from datetime import timedelta
from slack.errors import SlackApiError
from slack import WebClient
# import user-generated file
import Preprocess
import ParseData
import StockChanges
from pysrc.database import show
from pysrc.database import getUserInfo

myToken = "xoxb-1957223267923-1942727154343-nL4gXWXZ85PsgfICDuJExYdM"
myChannel = "#stock-investment"
client = WebClient(token=myToken)
# Change the api call to ephemeral message api


def special():
    IDList = getUserInfo.getID()
    NameList = getUserInfo.getName()
    MaxList = getUserInfo.getMax()
    MinList = getUserInfo.getMin()
    for info_rep in range(len(IDList)):
        # Get ID and Name of each user
        user_id = IDList[info_rep]
        user_name = NameList[info_rep]
        user_max = MaxList[info_rep]
        user_min = MinList[info_rep]
        print("ID: "+user_id+" | MAX: "+str(user_max)+" | MIN: "+str(user_min))
        SampleStockList = show.show(user_id, user_name)
        outputList = StockChanges.moniterStock(
            SampleStockList, user_max, user_min)
        print(outputList)
        # pickle로 file 읽어들인 후 TimeStamp Dictionary에 저장하기
        currentTime = datetime.now().time()
        with open("TimeStamp.pkl", "rb") as file:
            try:
                TimeStamp = pickle.load(file)
            except EOFError:
                TimeStamp = {}
        file.close()
        if (TimeStamp.get(user_name) == None):  # user_name이 처음 주식을 조회했을 때
            TimeStamp[user_name] = outputList
            array = TimeStamp.get(user_name)
            with open("TimeStamp.pkl", "wb") as file:
                pickle.dump(TimeStamp, file)  # Local pkl file로 save
            file.close()
            for stock in array:
                msg = configure_message(user_name, stock)
                post_message(myChannel, msg)
                print("specialSchedule.py | Node.js Status : Normal(200)")
        else:  # user_name이 기존에 조회한 목록이 존재할 때
            array = TimeStamp.get(user_name)
            index = 0
            for stock in array:  # 변화가 있다고 판단된 종목 전체 순회
                # print(currentTime)
                time_A = timedelta(
                    hours=stock[0].hour, minutes=stock[0].minute, seconds=stock[0].second)
                time_B = timedelta(
                    hours=currentTime.hour, minutes=currentTime.minute, seconds=currentTime.second)
                elapsedTime = (time_B - time_A).total_seconds()/60
                # print(elapsedTime)
                if (elapsedTime >= 30):  # 30분 이상이 지났을 때
                    msg = configure_message(user_name, stock)
                    post_message(myChannel, msg)
                    TimeStamp[user_name][index][0] = currentTime
                    with open("TimeStamp.pkl", "wb") as file:
                        pickle.dump(TimeStamp, file)  # Local pkl file로 save
                    file.close()
                    print("specialSchedule.py | Node.js Status : Normal(200)")
                else:
                    print("specialSchedule.py | Node.js Status : Waiting(300)")
                index += 1


def post_message(channel, text):
    try:
        response = client.api_call(
            api_method='chat.postMessage',
            json={'channel': channel, 'text': text})
    except SlackApiError as e:
        assert e.response["error"]


def configure_message(user_name, outputList):
    text = user_name + " 님, 관심종목에 변동사항이 발생했습니다\n"
    text = text + "현재 시각: "+outputList[0].strftime("%H:%M:%S")+"\n"
    text = text + outputList[1] + "(" + str(outputList[2]) + ")\n"
    text = text + "전일 대비 " + str(outputList[3]) + "%\n"
    text = text + "현재 시가: " + outputList[4] + " KRW"
    return text


if __name__ == '__main__':
    sys.setrecursionlimit(50000000)
    special()
