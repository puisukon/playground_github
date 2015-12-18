
import urllib
from bs4 import BeautifulSoup

stockList = ['BCP']
url = 'http://www.set.or.th/set/historicaltrading.do?symbol={0}&page={1}&language=th&country=TH&type=trading'
priceDate = []
priceList = {}
def getPrice(stock,pageNo):
    htmlFile = urllib.urlopen(url.format(stock,pageNo)).read()
    soup = BeautifulSoup(htmlFile,'html.parser')
    table = soup.find(attrs={'class':'table table-hover table-info'})
    for each in table.find_all('tr'):
            if len(each.findAll('td')) > 4 :
                    td = each.findAll('td')
                    dateStr = td[0].text.split('/')[2]+td[0].text.split('/')[1]+td[0].text.split('/')[0]
##                    print dateStr," : ",td[4].text
                    priceList[dateStr] = float(td[4].text)
                    priceDate.append(dateStr)


for each in stockList:
    print each
    getPrice(each,0)
    getPrice(each,1)
    getPrice(each,2)


yesterdayPrice = priceList[priceDate[len(priceDate) - 1]]
countDayPlus = 0
countDayMinus = 0
onHand = 0
gain = 0
totalGain = 0
for each in range(len(priceDate)-1,-1,-1):
##    print priceDate[each],priceList[priceDate[each]]
    date = priceDate[each]
    price = priceList[date]
    priceChange = priceList[priceDate[each]] - yesterdayPrice
##    print priceChange
    if priceChange > 0 :
        countDayPlus += 1
        if countDayPlus == 3 :
            if onHand == 0:
                onHand = price
                print date,price,"+++++" ,priceChange ," : ",countDayPlus   ," <<<<<<<<<<<<<<<<< BUY " , price
            else:
                print date,price,"+++++" ,priceChange ," : ",countDayPlus   ," <<< BUY" , price
        else:
            print date,price,"+++++" ,priceChange ," : ",countDayPlus
        countDayMinus = 0
    elif priceChange < 0:
        countDayMinus += 1
        if countDayMinus == 3:
            if onHand <> 0:
                gain = price - onHand
                totalGain += gain
                onHand = 0
                print date,price,"-----" ,priceChange ," : " , countDayMinus," <<<<<<<<<<<<<<<<< SELL" , price , gain , totalGain
            else:
                print date,price,"-----" ,priceChange ," : " , countDayMinus," <<< SELL" , price
        else:
            print date,price,"-----" ,priceChange ," : " , countDayMinus
