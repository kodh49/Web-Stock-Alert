import requests
import pandas as pd
from bs4 import BeautifulSoup

stock_type = {
    'kospi': 'stockMkt',
    'kosdaq': 'kosdaqMkt'
}

# Preprocess the datatable from finance excel file


def getDownloadStock(market_type=None):
    market_type = stock_type[market_type]
    df = pd.read_html(
        'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&marketType='+market_type, header=0)[0]
    df = df.rename(columns={'회사명': 'name', '종목코드': 'code'})
    return df

# define a function to get a code from company name


def getDownloadKospi():
    df = getDownloadStock('kospi')
    df.code = df.code.map('{:06d}'.format)
    return df


def getDownloadKosdaq():
    df = getDownloadStock('kosdaq')
    df.code = df.code.map('{:06d}'.format)
    return df


kospi_df = getDownloadKospi()
kosdaq_df = getDownloadKosdaq()

code_df = pd.concat([kospi_df, kosdaq_df])
code_df = code_df[['name', 'code']]


def getCode(ProductName):
    code = code_df.query("name=='{}'".format(ProductName))[
        'code'].to_string(index=False)
    code = code.strip()
    return code
