# Public Data Portal

https://www.data.go.kr/


- [Request (2021.12.04)]()


## [Request (2021.12.04)]()

- Why error? You should **Choose the decoding key**. Don't encode already encoded key again

#### Key.py
```python
encodingKey = ''
decodingKey = ''
```

#### Request.py
```python
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

response = requests.get(url, params=params)     # require encoding key, not decoding key
print(response.content)
```

#### Output
```xml
b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<response>\n    <header>\n        <resultCode>00</resultCode>\n        <resultMsg>NORMAL SERVICE.</resultMsg>\n    </header>\n    <body>\n        <numOfRows>10</numOfRows>\n        <pageNo>1</pageNo>\n        <totalCount>0</totalCount>\n        <items/>\n    </body>\n</response>\n'
```