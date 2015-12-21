
import urllib
from bs4 import BeautifulSoup


############# Method 1 ####################
############# buy when + 3 day , sell when - 3 days ####################
############# Method 1 ####################

stockList = ['SCCC']
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
                    priceList[dateStr] = float(td[4].text)
                    priceDate.append(dateStr)

def method1(priceList):
    pass

for eachStock in stockList:
    print eachStock
    getPrice(each,0)
    getPrice(each,1)
    getPrice(each,2)


yesterdayPrice = priceList[priceDate[len(priceDate) - 1]]
countDayPlus = 0
countDayMinus = 0
onHand1 = 0
onHand2 = 0
gain1 = 0
gain2 = 0
totalGain1 = 0
totalGain2 = 0
for each in range(len(priceDate)-1,-1,-1):
    date = priceDate[each]
    price = priceList[date]
    priceChange = priceList[priceDate[each]] - yesterdayPrice
    if priceChange > 0 :
        countDayPlus += 1
        if countDayPlus == 3 :
            if onHand1 == 0:
                onHand1 = price
                print date,price,"+++++" ,priceChange ," : ",countDayPlus   ," <<<<<<<<M1<<<<<<<<< BUY  " , price
            else:
                print date,price,"+++++" ,priceChange ," : ",countDayPlus   ," <<<M1 BUY" , price

            if onHand2 <> 0:
                gain2 = price - onHand2
                totalGain2 += gain2
                onHand2 = 0
                print date,price,"+++++" ,priceChange ," : " , countDayMinus," <<<<<<<M2<<<<<<<<<< SELL" , price , gain2 , totalGain2
            else:
                print date,price,"+++++" ,priceChange ," : " , countDayMinus," <<<M2 SELL" , price
                
        else:
            print date,price,"+++++" ,priceChange ," : ",countDayPlus
        countDayMinus = 0
    elif priceChange < 0:
        countDayMinus += 1
        if countDayMinus == 3:
            if onHand1 <> 0:
                gain1 = price - onHand1
                totalGain1 += gain1
                onHand1 = 0
                print date,price,"-----" ,priceChange ," : " , countDayMinus," <<<<<<<M1<<<<<<<<<< SELL" , price , gain1 , totalGain1
            else:
                print date,price,"-----" ,priceChange ," : " , countDayMinus," <<<M1 SELL" , price

            if onHand2 == 0:
                onHand2 = price
                print date,price,"-----" ,priceChange ," : ",countDayPlus   ," <<<<<<<<M2<<<<<<<<< BUY  " , price
            else:
                print date,price,"-----" ,priceChange ," : ",countDayPlus   ," <<<M2 BUY" , price

        else:
            print date,price,"-----" ,priceChange ," : " , countDayMinus
        countDayPlus = 0
    else :
        print priceDate[each],priceList[priceDate[each]],"====="
    yesterdayPrice = priceList[priceDate[each]]


print "{0} : M1 = {1} %, M2 = {2} %".format(eachStock,round(totalGain1/price*100,2),round(totalGain2/price*100,2))
