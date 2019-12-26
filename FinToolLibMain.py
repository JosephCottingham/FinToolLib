import requests
from datetime import datetime
import math

class stock:
    def __init__(self, ticker):
        self.ticker = ticker

    def gNum(self):
        urlEPS = 'https://financialmodelingprep.com/api/v3/financials/income-statement/' + self.ticker
        urlShareholdersEquity = 'https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/' + self.ticker
        urlShares = 'https://financialmodelingprep.com/api/v3/company/profile/' + self.ticker

        byteDataIncome = requests.get(urlEPS)
        byteDataShareholdersEquity = requests.get(urlShareholdersEquity)
        byteDataShares = requests.get(urlShares)

        dataIncome = str(byteDataIncome.content)
        dataBalance = str(byteDataShareholdersEquity.content)
        DataShares = str(byteDataShares.content)

        if len(dataIncome) > 10 and len(dataBalance) > 10 and len(DataShares) > 10:
            startLocationEPS = dataIncome.find("EPS Diluted") + 16
            endLocationEPS = dataIncome.find('",', startLocationEPS)
            EPS = dataIncome[startLocationEPS:endLocationEPS]

            startLocationIncomeDate = dataIncome.find("date") + 9
            endLocationIncomeDate = dataIncome.find('",', startLocationIncomeDate)
            if endLocationIncomeDate - startLocationIncomeDate < 8:
                incomeDate = datetime.strptime(dataIncome[startLocationIncomeDate:endLocationIncomeDate], "%Y-%m")
            else:
                incomeDate = datetime.strptime(dataIncome[startLocationIncomeDate:endLocationIncomeDate], "%Y-%m-%d")

            startLocationBalanceDate = dataBalance.find("date") + 9
            endLocationBalanceDate = dataBalance.find('",', startLocationBalanceDate)
            if endLocationBalanceDate - startLocationBalanceDate < 8:
                balanceDate = datetime.strptime(dataBalance[startLocationBalanceDate:endLocationBalanceDate], "%Y-%m")
            else:
                balanceDate = datetime.strptime(dataBalance[startLocationBalanceDate:endLocationBalanceDate],
                                                "%Y-%m-%d")

            startLocationShareholdersEquity = dataBalance.find("Total shareholders equity") + 30
            endLocationShareholdersEquity = dataBalance.find('",', startLocationShareholdersEquity)
            ShareholdersEquity = dataBalance[startLocationShareholdersEquity:endLocationShareholdersEquity]

            startLocationPrice = DataShares.find("price") + 9
            endLocationPrice = DataShares.find(',', startLocationPrice)
            price = DataShares[startLocationPrice:endLocationPrice]

            startLocationDividend = dataIncome.find("Dividend per Share") + 23
            endLocationDividend = dataIncome.find('",', startLocationDividend)
            if dataIncome[startLocationDividend:endLocationDividend] != "":
                dividend = 100 * (float(dataIncome[startLocationDividend:endLocationDividend]) / float(price))
            else:
                dividend = 0

            startLocationMarketcap = DataShares.find("mktCap") + 11
            endLocationMarketcap = DataShares.find('",', startLocationMarketcap)
            Marketcap = DataShares[startLocationMarketcap:endLocationMarketcap]
            self.gNum = math.sqrt(15 * 1.5 * (float(EPS)) * (float(ShareholdersEquity) / (float(Marketcap) / float(price))))
            return self.gNum
if __name__ == '__main__':
    x = stock(input('input ticker'))
    print('gNum: ' + str(x.gNum()))