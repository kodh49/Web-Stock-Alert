import requests
from bs4 import BeautifulSoup
import json
import schedule
import sys
import os
from datetime import datetime
from slack.errors import SlackApiError
from slack import WebClient
from collections import OrderedDict
# import user-generated file
import ParseData
import StockChanges
import Preprocess
from pysrc.database import show
from pysrc.database import getUserInfo

# Read from csv file
myToken = "xoxb-1957223267923-1942727154343-nL4gXWXZ85PsgfICDuJExYdM"
myChannel = "#stock-investment"
client = WebClient(token=myToken)

# Send message to the channel with predetermined text

# 9시 ~ 15시 30분까지 시간 체크해서 받아오기


def post_message(channel, myJSON):
    try:
        response = client.chat_postMessage(
            channel=channel,
            blocks=myJSON
        )
    except SlackApiError as e:
        assert e.response["error"]


def writeJSON(user_name, outputList):
    RegularBlockKit = OrderedDict()
    BlockKit = []
    section = OrderedDict()
    section["type"] = "section"
    section["text"] = OrderedDict()
    section["text"]["type"] = "mrkdwn"
    section["text"]["text"] = "현재 시각 " + datetime.now().time().strftime("%H:%M") + \
        " 기준 " + user_name + "님의 관심 종목 시세를 알려드립니다.\n"
    BlockKit.append(section)
    for i in range(len(outputList)):
        section = OrderedDict()
        divider = OrderedDict()
        divider["type"] = "divider"
        BlockKit.append(divider)
        section["type"] = "section"
        section["text"] = OrderedDict()
        section["text"]["type"] = "mrkdwn"
        data = "*"+outputList[i][1] + "(" + str(outputList[i][2]) + ")* "
        if outputList[i][3] >= 0:
            data = data + "+" + \
                str(outputList[i][3])+"%\n"+outputList[i][4] + " KRW"
        else:
            data = data + str(outputList[i][3]) + \
                "%\n"+outputList[i][4] + " KRW"
        section["text"]["text"] = data
        BlockKit.append(section)
    msgJson = json.dumps(BlockKit, ensure_ascii=False, indent="\t")
    return msgJson


def regular():
    IDList = getUserInfo.getID()
    NameList = getUserInfo.getName()
    length = len(IDList)
    print(length)
    for info_rep in range(length):
        user_id = IDList[info_rep]
        user_name = NameList[info_rep]
        SampleStockList = show.show(user_id, user_name)
        outputList = StockChanges.moniterStock(SampleStockList, 0.0001, 0.0001)
        msgJson = writeJSON(user_name, outputList)
        print("regularSchedule.py | Response<200>")
        post_message(myChannel, msgJson)


if __name__ == '__main__':
    regular()
