# 공공데이터포털 > 오픈API > 금융위원회_채권발행정보
# https://www.data.go.kr/data/15043421/openapi.do



# 2. Read data on plural pages


# 2.1 Required modules

import requests                 # send assembled URL and get API response 
from bs4 import BeautifulSoup   # get suitable format with pandas dataframe from raw XML data
import pandas as pd             # convert refined XML data to dataframe format for saving as a .csv file
import time                     # use to measure time performance and react the request freqency limmit if it exists
import math                     # calculate numbers related with pageNo, numOfRows
import os                       # check if the .csv file has been successfully saved

import Key                      # call keys, the file path to save and the list of data columns from Key.py


###################################### 2.2 SETTING ######################################   # can you feel my love?

# (1) Set url for requesting data : append params to url
url = 'http://apis.data.go.kr/1160100/service/GetBondTradInfoService/getIssuIssuItemStat'
params = {
    'serviceKey' : Key.decodingKey,                                                         # .encodingKey occurs an error; SERVICE_KEY_IS_NOT_REGISTERED_ERROR
    'pageNo' : '1',                                                                         # fix 1
    'numOfRows' : '1',                                                                      # fix 1
    'resultType' : 'xml',                                                                   # all the below code assumes xml, not json
    # 'basDt' : '20201116',
    # 'crno' : '1101110084767',
    # 'bondIsurNm' : '국동'
}

# (2) Set the row number to start and end
startRow = 1
endRow = 100                                                                                # put small number during test (max : 38960)

# (3) Set the .csv file path to save data
fileName = "test"                                                                           # don't include ".csv"

# (4) Set sleep period between each request (sec)
sleepTime = 0                                                                               # set if request frequency limmit exists

# (5) Set columns to contain data needed
df = pd.DataFrame(columns = Key.columns)                                                    # may modify column names in Key.py whatever you need

#########################################################################################


# 2.2.1 Background operation related with 2.2 Setting

# Find where the startPage and endPage are
startPage = math.floor(startRow / int(params['numOfRows']))                                 # floor() : rounding down
endPage = math.ceil(endRow / int(params['numOfRows']))                                      # ceil() : rounding up
totalPage = endPage - startPage + 1
measurePerfTerm = max(1, totalPage / 10)                                                    # check the completion ratio 10 times 

# Mark the starting and ending row numbers into the file name
path = Key.path + '/' + fileName + '_' + str(startRow) + "_" + str(endRow) + ".csv"         # Key.path is initially declared in Key.py

# Generate a new list that contains string such like "item.****.text"
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

print("데이터 다운로드를 시작합니다.")
startTime = time.perf_counter()                                                             # set the reference point to measure performance
for i in range(startPage, endPage + 1) :                                                    # endPage + 1 → run until endPage

    # print(i)                                                                              # test : ok

    # Measure the completion ratio and avoid the data request frequency limmit if it exists (180 sec.)
    if (i != startPage) and (i % measurePerfTerm == 0 or i == endPage)  :
        elapseTime = time.perf_counter() - startTime
        completionRatio = (i - startPage + 1) / totalPage
        print("{:0,.1f}분 남았습니다. (진행률 : {:0,.1f}%)".format((elapseTime / completionRatio - elapseTime) / 60, completionRatio * 100))
        # time.sleep(sleepTime)

    # Refine raw XML data to be suitable with pandas dataframe
    params['pageNo'] = i
    response = requests.get(url, params=params)                                             # doesn't require encoding key, but decoding key
    # print(response.content)                                                               # test : .content is necessary, not use only response
    soup = BeautifulSoup(response.content, "html.parser")                                   # remove 'b and run line replacement

    # Stack data into pandas data frame (on memory)
    for item in soup.findAll("body") :                                                      # all data are located between <body> and </body> tags
        temp = []
        for j in range(0, len(soupColumns)) :
            if eval(soupColumns[j]) != None :                                               # check if the tag exists
                temp.append(eval(soupColumns[j]))                                           # eval() : "item.numofrows.text" to item.numofrows.text
            else :
                temp.append("")                                                             # fill "" when there is no data in the tag
            # print(temp)                                                                   # test : ok - for finding where an error occurs
        df.loc[i] = temp


# 2.4 Loop to request missing data 

missingPage = (endPage - startPage + 1) - len(df)                                             # get the number of missing data
measurePerfTerm = max(1, totalPage / 10)                                                    # check the completion ratio 10 times
if missingPage == 0 :
    print("누락된 데이터가 없습니다.")
else :
    print("누락된 데이터({}건)의 추가 다운로드를 시작합니다.".format(missingPage))
    startTime = time.perf_counter()                                                             # set the reference point to measure performance
    for i in range(startPage, endPage + 1) :                                                    # endPage + 1 → run until endPage

        # Measure the completion ratio and avoid the data request frequency limmit if it exists (180 sec.)
        if (i != startPage) and (i % measurePerfTerm == 0 or i == endPage)  :
            elapseTime = time.perf_counter() - startTime
            completionRatio = (i - startPage + 1) / totalPage
            print("{:0,.1f}분 남았습니다. (진행률 : {:0,.1f}%)".format((elapseTime / completionRatio - elapseTime) / 60, completionRatio * 100))
            # time.sleep(sleepTime)

        # find if missing data
        if i not in df['pageno'] :

            # Refine raw XML data to be suitable with pandas dataframe 
            params['pageNo'] = i
            response = requests.get(url, params=params)                                             # doesn't require encoding key, but decoding key
            # print(response.content)                                                               # test : .content is necessary, not use only response
            soup = BeautifulSoup(response.content, "html.parser")                                   # remove 'b and run line replacement

            # stack data into pandas data frame (on memory)
            for item in soup.findAll("body") :                                                      # all data are located between <body> and </body> tags
                temp = []
                for j in range(0, len(soupColumns)) :
                    if eval(soupColumns[j]) != None :                                               # check if the tag exists
                        temp.append(eval(soupColumns[j]))                                           # eval() : "item.numofrows.text" to item.numofrows.text
                    else :
                        temp.append("")                                                             # fill "" when there is no data in the tag
                    # print(temp)                                                                   # test : ok - for finding where an error occurs
                df.loc[i] = temp


# 2.5 Save data as a .csv fie

# print(df)                                                                                 # test : ok
if os.path.isfile(path) :                                                                   # to prevent overwriting the file
    print("이미 같은 이름의 파일이 존재합니다. (", path, ")")
    # don't need to run the loop again, just change the old file's name
else :
    df.to_csv(path, encoding = 'utf-8-sig')
    if os.path.isfile(path) :                                                               # I am too hospitable, you must have won a man like the lotto!
        print("데이터가 정상적으로 저장되었습니다. (", path, ")")
    else :
        print("데이터가 정상적으로 저장되지 않았습니다.")