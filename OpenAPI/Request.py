import requests
import Key              # call keys from Key.py

url = 'http://apis.data.go.kr/1160100/service/GetBondTradInfoService/getIssuIssuItemStat'
params = {
    'serviceKey' : Key.decodingKey,
    'pageNo' : '1',
    'numOfRows' : '10',
    'resultType' : 'xml',
    'basDt' : '20201116',
    'crno' : '1101110084767',
    'bondIsurNm' : '국동'
}

response = requests.get(url, params=params)
print(response.content)