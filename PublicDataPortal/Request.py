# 공공데이터포털 > 오픈API > 금융위원회_채권발행정보
# https://www.data.go.kr/data/15043421/openapi.do


import requests
import Key                                      # call keys from Key.py

url = 'http://apis.data.go.kr/1160100/service/GetBondTradInfoService/getIssuIssuItemStat'
params = {
    'serviceKey' : Key.decodingKey,             # .encodingKey occurs an error; SERVICE_KEY_IS_NOT_REGISTERED_ERROR
    'pageNo' : '1',
    'numOfRows' : '10',
    'resultType' : 'xml',
    'basDt' : '20201116',
    'crno' : '1101110084767',
    'bondIsurNm' : '국동'
}

response = requests.get(url, params=params)     # doesn't require encoding key, but decoding key
print(response.content)