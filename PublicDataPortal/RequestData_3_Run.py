"""
<프로그램명>
아내를 위한 공공데이터포털 데이터 다운로드 도우미

<버전>
3.0

<작성일>
2022.09.21

<프로그램 설명>
- 개     요 : 공공데이터포털(data.go.kr)에서 대량의 데이터를 보다 쉽게 다운로드 받기 위한 유틸리티입니다.
- 주요 취지 : 남편이 아내에게 두고두고 생색 내기 위하여 만들었습니다.
- 개발 환경 : Windows 8 / Python 3.9 (32-bit)
- 구     성 : Run.py, Key.py, Operation.py (3개 파일)

<사용법>
- 실행 전 준비 사항
  · Key.py          : 동일한 사용자인 경우 대상 데이터가 바뀌더라도 최초 1회만 작성 (Key는 동일함)
  · Run.py(본 파일) : ### SETTING ### 내의 변수 기입
- 실행              : Run.py (본 파일)
- 테스트 모드 실행   : Operation.py 실행 (콘솔 로그 출력이 추가되는 이외에 나머지 기능은 모두 같음)

<팁>
- 다른 데이터 자료를 다운로드받을 경우 본 파일만 수정하시면 됩니다(복사하여 다른 이름으로 저장하길 권고합니다).
- 최초 작동시 트래픽 한도를 오류로 낭비하지 않도록 page['end']에 작은 수를 입력하세요(ex. 10).
# - 같은 범위에 대하여 프로그램을 재실행시 빈 데이터만 이어서 다운로드합니다. (개발중)
"""


import Key                      as Key
import RequestData_3_Operation  as Operation


###################################### SETTING ##########################################

# (1) 데이터 제목 : 공공데이터포털 > 오픈API > 금융위원회_채권발행정보 > 발행자별발행종목현황조회
# (2) 페이지 링크 : https://www.data.go.kr/data/15043421/openapi.do

# (3) 요청주소
url = 'http://apis.data.go.kr/1160100/service/GetBondTradInfoService/getIssuIssuItemStat'

# (4) pageNo의 시작과 끝, 간격
page = {
    'start' : 1,
    'end' : 10,                                                                             # ★ 테스트시에는 충분히 작은 숫자를 대입 : ex. 10
    'interval' : 1,
}

# (5) 데이터 저장 경로 및 파일명
path = {
    'path' : '.',                                                                           # . : 현재 위치를 의미
    'fileName' : '발행자별발행종목현황조회',                                                  # 확장자 없이 입력
}

# (6) 요청 시간 간격 (초)
sleepTime = 0                                                                               # 단기적인 트래픽 제한이 없다면 0으로 유지

# (7) 요청변수
params = {
    'serviceKey' : Key.decodingKey,                                                         # .encodingKey로 설정시 오류 발생; SERVICE_KEY_IS_NOT_REGISTERED_ERROR
    'pageNo' : '1',                                                                         # 1로 고정
    'numOfRows' : '1',                                                                      # 페이지당 결과수 (복수값 적용은 개발중)
    'resultType' : 'xml',                                                                   # xml/json 중에서 선택 가능하나, 본 프로그램은 xml만을 지원함
    # 'basDt' : '20201116',
    # 'crno' : '1101110084767',
    # 'bondIsurNm' : '국동'
}

# (8) 출력결과
columns = [
    "resultCode",
    "resultMsg",
    "numofrows",
    "pageno",
    "totalCount",
    "basDt",
    "crno",
    "bondIsurNm",
    # add more columns
]

#########################################################################################


# 실행
if __name__ == "__main__" :

    Operation.Operation(
        url,
        page,
        path,
        sleepTime,
        params,
        columns
    )