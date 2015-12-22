#!/usr/bin/python 
import urllib
from bs4 import BeautifulSoup

#   Intend to calculate MA ( Moving Average ) of the stock
stockList = [
    'ADVANC',
'INTUCH',
'JAS',
'DTAC',
'CPALL',
'KBANK',
'BDMS',
'AOT',
'CSS',
'PTT',
'SCB',
'KTB',
'TKN',
'TCAP',
'BBL',
'SCC',
'EPG',
'IFEC',
'BH',
'PTTEP',
'TOP',
'MINT',
'CPN',
'ITD',
'PTTGC',
'MTLS',
'TU',
'TMB',
'MAX',
'TASCO',
'IRPC',
'K',
'VIBHA',
'CPF',
'TIPCO',
'SAWAD',
'CK',
'THCOM',
'LH',
'BA',
'SCI',
'ASEFA',
'BANPU',
'SUPER',
'BTS',
'INET',
'AMATAV',
'GLOW',
'COM7',
'JTS',
'MAJOR',
'GUNKUL',
'HMPRO',
'TPIPL',
'SAMART',
'TWPC',
'BCP',
'STEC',
'STPI',
'LPH',
'S',
'WHA',
'SCCC',
'SIRI',
'DELTA',
'TTW',
'MFEC',
'SPALI',
'QH',
'ROBINS',
'AAV',
'CENTEL',
'EGCO',
'IVL',
'AJD',
'BEAUTY',
'GPSC',
'SPRC',
'TTCL',
'RATCH',
'BCH',
'EARTH',
'HFT',
'PT',
'CPR',
'NUSA',
'PLANB',
'BEC',
'TACC',
'EA',
'J',
'HANA',
'PIMO',
'KTC',
'KCE',
'UNIQ',
'AUCT',
'BLAND',
'RP',
'M',
'PTG',
'SF',
'ICHI',
'TTA',
'CHG',
'BLA',
'THANI',
'SGP',
'DEMCO',
'SAPPE',
'PRAKIT',
'KKP',
'SVI',
'BIGC',
'LPN',
'PS',
'TNH',
'BAFS',
'ASIMAR',
'VNG',
'EFORL',
'TSE',
'VIH',
'TVO',
'MCS',
'AP',
'BJCHI',
'NYT',
'SCN',
'TRC',
'GEL',
'ECF',
'VGI',
'AIT',
'TISCO',
'SR',
'MONO',
'TAPAC',
'BR',
'WICE',
'UWC',
'EMC',
'THREL',
'LIT',
'CKP',
'TICON',
'TFG',
'SPCG',
'WIIK',
'ERW',
'ASK',
'SOLAR',
'THAI',
'FPI',
'STA',
'PCA',
'GL',
'TVT',
'IEC',
'BWG',
'TAKUNI',
'T',
'SENA',
'BTC',
'LHBANK',
'PDI',
'MALEE',
'JWD',
'IRCP',
'DCC',
'DCORP',
'ASP',
'CBG',
'MEGA',
'TIP',
'ILINK',
'SYNTEC']
url = 'http://www.set.or.th/set/historicaltrading.do?symbol={0}&page={1}&language=th&country=TH&type=trading'
priceDate = []
priceList = {}
MA3List = {}
MA7List = {}
def getPrice(stock,pageNo):
    htmlFile = urllib.urlopen(url.format(stock,pageNo)).read()
    soup = BeautifulSoup(htmlFile,'html.parser')
    table = soup.find(attrs={'class':'table table-hover table-info'})
    if table:
        for each in table.find_all('tr'):
            if len(each.findAll('td')) > 4 :
                td = each.findAll('td')
                dateStr = td[0].text.split('/')[2]+td[0].text.split('/')[1]+td[0].text.split('/')[0]
                if td[4].text.count("-") == 0 :
                    priceList[dateStr] = float(td[4].text)
                    priceDate.append(dateStr)

def findMA3():
    lastN = []
    for each in range(len(priceDate)-1,-1,-1):
        date = priceDate[each]
        price = float(priceList[priceDate[each]])
        if len(lastN) == 3 :
            lastN.pop(0)
        lastN.append(price)
        MA3List[date] = round(sum(lastN)/len(lastN),3)

def findMA7():
    lastN = []
    for each in range(len(priceDate)-1,-1,-1):
        date = priceDate[each]
        price = float(priceList[priceDate[each]])
        if len(lastN) == 7 :
            lastN.pop(0)
        lastN.append(price)
        MA7List[date] = round(sum(lastN)/len(lastN),3)


for eachStock in stockList:
    print eachStock
    priceDate = []
    priceList = {}
    MA3List = {}
    MA7List = {}
    getPrice(eachStock,0)
    getPrice(eachStock,1)
    getPrice(eachStock,2)

    findMA3()
    findMA7()

    onHand = 0
    gain = 0
    totalGain = 0
    for each in range(len(priceDate)-1,-1,-1):
        if each < len(priceDate) - 10 :
            date = priceDate[each]
            price = float(priceList[date])
            prePrice = float(priceList[priceDate[each + 1]])
            preprePrice = float(priceList[priceDate[each + 2]])
            preDate = priceDate[each + 1]
            if MA3List[date] > MA7List[date] and MA3List[preDate] < MA7List[preDate]:
                if onHand == 0:
                    onHand = prePrice
                    print date,price,MA3List[date],MA7List[date] , " +++++ UP , Buy ",prePrice
                else:
                    print date,price,MA3List[date],MA7List[date] , " +++++ UP"
            elif MA3List[date] < MA7List[date] and MA3List[preDate] > MA7List[preDate]:
                if onHand <> 0 :
                    gain = prePrice - onHand
                    totalGain += gain
                    onHand = 0
                    print date,price,MA3List[date],MA7List[date] , " ----- Down, SELL", prePrice,gain,totalGain
                else:
                    print date,price,MA3List[date],MA7List[date] , " ----- Down"
            elif onHand <> 0 and (prePrice - onHand) / prePrice * 100 < -1.0 :
                gain = prePrice - onHand
                totalGain += gain
                onHand = 0
                print "Cut Loss ",prePrice,gain, totalGain, (prePrice - preprePrice) / prePrice * 100
            else:
                pass
##                print date,price,MA3List[date],MA7List[date]
    print eachStock,price,round(float(totalGain)/price* 100.0,2)," %"
    print " ####################################################################"
    

