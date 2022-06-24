import Preprocess


def isValid(stockName):
    stock = Preprocess.getCode(stockName)
    print(stock)


if __name__ == '__main__':
    isValid("삼성전자")
