# 공공데이터포털 > 오픈API > 금융위원회_채권발행정보
# https://www.data.go.kr/data/15043421/openapi.do



# 2. Read data on plural pages


# 2.1 Required modules

import requests                                 # send assembled URL and get API response 
from bs4 import BeautifulSoup                   # get suitable format with pandas dataframe from raw XML data
import pandas as pd                             # convert refined XML data to dataframe format for saving as a .csv file
import time                                     # use to measure time performance and react the request freqency limmit if it exists
import math                                     # calculate numbers related with pageNo, numOfRows
import os                                       # check if the .csv file has been successfully saved

import Key                                      # call keys, the file path to save and the list of data columns from Key.py


###################################### 2.2 SETTING ######################################   # can you feel my love?

# (1) Set url for requesting data : append params to url
url = 'http://apis.data.go.kr/1160100/service/GetBondTradInfoService/getIssuIssuItemStat'
params = {
    'serviceKey' : Key.decodingKey,                                                         # .encodingKey occurs an error; SERVICE_KEY_IS_NOT_REGISTERED_ERROR
    'pageNo' : '1',                                                                         # fix 1
    'numOfRows' : '1',                                                                      # fix 1
    'resultType' : 'xml',
    # 'basDt' : '20201116',
    # 'crno' : '1101110084767',
    # 'bondIsurNm' : '국동'
}

# (2) Set the .csv file path to save data
Key.path += '/test.csv'                                                                     # Key.path is initially declared in Key.py

# (3) Set the number how many times request data
total = 20                                                                                  # put small number when test (max : 38960)

# (4) Set sleep period between each request (sec)
sleepTime = 0                                                                               # set if request frequency limmit exists

# (5) Set columns to contain data needed
df = pd.DataFrame(columns = Key.columns)                                                    # may modify column names in Key.py whatever you need

#########################################################################################


# 2.2.1 Background operation related with 2.2 Setting

# Determine how many times the loop runs
maxPage = math.ceil(total / int(params['numOfRows']))                                       # ceil : rounding up

# Generate a new list that contains string such like "item.numofrows.text"
soupColumns = []
for c in Key.columns :
    soupColumns.append("item." + c + ".text")
# print(soupColumns)                                                                        # test : ok


# Test : request data of 1 set
# response = requests.get(url, params=params)                                               # doesn't require encoding key, but decoding key
# print(response.content)                                                                   # test to check if the raw XML data arrive well
# soup = BeautifulSoup(response.content, "html.parser")                                     # remove 'b and run line replacement
# print(soup)                                                                               # test : ok


# 2.3 Loop to request data continously

startTime = time.perf_counter()
for i in range(1, maxPage + 1) :                                                            # maxPage + 1 → run until maxPage

    # Measure the completion ratio and avoid the data request frequency limmit if it exists (180 sec.)
    if i != 1 :
        elapseTime = time.perf_counter() - startTime
        completionRatio = i / maxPage
        print("{:0,.1f}분 남았습니다. (진행률 : {:0,.1f}%)".format((elapseTime / completionRatio - elapseTime) / 60, (i / maxPage) * 100))
        # sleep(sleepTime)

    # Refine raw XML data to be suitable with pandas dataframe
    params['pageNo'] = i
    response = requests.get(url, params=params)                                             # doesn't require encoding key, but decoding key
    # print(response.content)                                                               # test : .content is necessary, not use only response
    soup = BeautifulSoup(response.content, "html.parser")                                   # remove 'b and run line replacement

    for item in soup.findAll("body") :                                                      # all data are located between <body> and </body> tags
        temp = []
        for j in range(0, len(soupColumns)) :
            temp.append(eval(soupColumns[j]))                                               # eval() : "item.numofrows.text" to item.numofrows.text
            # print(temp)                                                                   # test : ok - for finding where an error occurs
        df.loc[i - 1] = temp


# 2.4 Save data as a .csv fie

# print(df)                                                                                 # test : ok
df.to_csv(Key.path, encoding = 'utf-8-sig')
if os.path.isfile(Key.path) :                                                               # I am too hospitable, you must have won a man like the lotto!
    print("데이터가 정상적으로 저장되었습니다. (", Key.path, ")")
else :
    print("데이터가 정상적으로 저장되지 않았습니다.")