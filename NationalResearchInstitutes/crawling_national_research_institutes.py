"""
<개요>
프로그램 설명 : 위키백과의 "정부출연연구기관" 페이지 및 관련 페이지들을 크롤링하여 데이터를 수집한 후 표로 정리합니다.
작성자 : 전생에 나라를 구한 아내의 남편

버  전 : 1.0
작성일 : 2023.05.05.

<사용방법>
- 그냥 본 파일을 실행하면 됨.

<왜 위키백과인가?>
- https://ko.wikipedia.org/wiki/정부출연연구기관 페이지에 리스트가 잘 정리되어 있음.
- 위 페이지의 각 항목 클릭시 기관별 정보가 규격화된 양식에 통일성 있게 정리되어 있음.
- 검색해보니 위키백과 크롤링 관련 게시물이 많은 걸로 봐서 크롤링에 호의적(?)인 것으로 보임.
"""

# Libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

# URLs
URL = 'https://ko.wikipedia.org/wiki/'
SEARCH_WORD = '정부출연연구기관'
SAVE_URL = '.'

# '/정부출연연구기관' 페이지에서 기관명 수집하기
res = requests.get(URL + SEARCH_WORD, timeout = 5)
soup = BeautifulSoup(res.text, 'html.parser')
mw_parser_output = soup.find('div', {'class': 'mw-parser-output'})

# 기관 리스트 정제하여 딕셔너리 key로 만들기
institutes = {}
for li in mw_parser_output.find_all('li'):
    a_tag = li.find('a')
    title_value = a_tag.get('title')                                            # ex) [[한국개발연구원]] → 반드시 title 속성이 있음
    if title_value is not None:                                                 # 외부링크는 title 속성 없음
        institutes[title_value] = {}

# 각 기관별 데이터 수집하기
details = ('설립일', '소재지', '위치', '원장', '상급기관', '산하기관', '웹사이트')
institutes_to_modify = []
INSTITUTES_LENGTH = len(institutes)
i = 0
for k, _ in institutes.items():
    # 진행상황
    i += 1
    print(f'({i}/{INSTITUTES_LENGTH}) {k} 크롤링 중')
    # 연결 문서가 없는 기관의 경우
    if ' (없는 문서)' in k :
        # k = k.replace(' (없는 문서)', '')                                      # .replace()만으로는 변경된 값을 저장하지 않는다
        # institutes[k] = {}                                                    # Causes a runtimeError: dictionary changed size during iteration
        institutes[k].update({'비고' : '문서 없음'})
        institutes_to_modify.append(k)
    # 연결 문서가 있는 기관의 경우
    else :
        res = requests.get(URL + k, timeout = 5)
        soup = BeautifulSoup(res.text, 'html.parser')
        try:
            infobox = soup.find('table', {'class': 'infobox'}).find_all('tr')   # 종종 'infobox'가 없다
            for info in infobox:
                if info.find('th') is not None :
                    k2 = info.find('th').text.strip()
                    if k2 in details :
                        v2 = info.find('td').text.strip()
                        institutes[k].update({k2 : v2})
        except:
            institutes[k].update({'비고' : '오류'})
    # 테스트
    # if IS_TEST and i == 10:
    #     break

# 문서 없는 기관명 수정 : ' (없는 문서)' 삭제
for institute in institutes_to_modify:
    institute_new = institute.replace(' (없는 문서)', '')
    institutes[institute_new] = institutes.pop(institute)

# 딕셔너리 → 데이터프레임 → CSV로 저장하기
df = pd.DataFrame.from_dict(data = institutes, orient = 'index')
df.loc[df['위치'].notnull(), '소재지'] = df['위치']
df = df.drop('위치', axis=1)
df.to_csv("national_research_institutes.csv", mode='w')
