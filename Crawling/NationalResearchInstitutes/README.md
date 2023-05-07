# [Web Crawling](../../README.md#web-crawling)


### \<List>

- [National Research Institutes' List (2023.05.06)](#national-research-institutes-list-20230506)


## [National Research Institutes' List (2023.05.06)](#list)

- She wanted to know a list of national research institutes located in Seoul.
  - I promised to keep her living in a happy dream forever.
- Crawled the ["정부출연기관" page](https://ko.wikipedia.org/wiki/정부출연연구기관) along with its associated ones from the Korean Wikipedia.
- The \<modified> version of the CSV file has been partially edited manually based on the original output.
- Use `https://www.convertcsv.com/csv-to-markdown.htm` to convert *CSV* to *markdown*.
- Future improvements
  - Add some crawling tasks for unstandardized linked pages

  <details>
    <summary>Codes : crawling_national_research_institutes.py</summary>

  ```py
  # 라이브러리
  import requests
  from bs4 import BeautifulSoup
  import pandas as pd
  ```
  ```py
  # URLs
  URL = 'https://ko.wikipedia.org/wiki/'
  SEARCH_WORD = '정부출연연구기관'
  SAVE_URL = '.'
  ```
  ```py
  # '/정부출연연구기관' 페이지에서 기관명 수집하기
  res = requests.get(URL + SEARCH_WORD, timeout = 5)
  soup = BeautifulSoup(res.text, 'html.parser')
  mw_parser_output = soup.find('div', {'class': 'mw-parser-output'})
  ```
  ```py
  # 기관 리스트 정제하여 딕셔너리 key로 만들기
  institutes = {}
  for li in mw_parser_output.find_all('li'):
      a_tag = li.find('a')
      title_value = a_tag.get('title')                                            # ex) [[한국개발연구원]] → 반드시 title 속성이 있음
      if title_value is not None:                                                 # 외부링크는 title 속성 없음
          institutes[title_value] = {}
  ```
  ```py
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
  ```
  ```py
  # 문서 없는 기관명 수정 : ' (없는 문서)' 삭제
  for institute in institutes_to_modify:
      institute_new = institute.replace(' (없는 문서)', '')
      institutes[institute_new] = institutes.pop(institute)
  ```
  ```py
  # 딕셔너리 → 데이터프레임 → CSV로 저장하기
  df = pd.DataFrame.from_dict(data = institutes, orient = 'index')
  df.loc[df['위치'].notnull(), '소재지'] = df['위치']
  df = df.drop('위치', axis=1)
  df.to_csv("national_research_institutes.csv", mode='w')
  ```
  </details>
  <details open>
    <summary>Output : Printing the progress of program</summary>

  ```
  (1/72) 한국개발연구원 크롤링 중
  (2/72) KDI 국제정책대학원 크롤링 중
  (3/72) 국토연구원 크롤링 중
  ……
  (72/72) 국립호남권생물자원관 (없는 문서) 크롤링 중
  ```
  </details>
  <details open>
    <summary>Output : national_research_institutes(modified).csv</summary>


  |기관명 |설립일|소재지|원장 |상급기관|웹사이트|비고 |
  |---|---|---|---|---|---|---|
  |한국전기연구원 |1976년 12월 29일|경상남도 창원시 성산구 전기의길 12 (성주동) | |과학기술정보통신부 |한국전기연구원 | |
  |광주과학기술원 | |광주광역시 북구 | ||http://www.gist.ac.kr/| |
  |대구경북과학기술원 | |대구광역시 달성군 현풍읍테크노중앙대로 333 | ||| |
  |한국천문연구원 | |대전 | ||www.kasi.re.kr| |
  |한국핵융합에너지연구원 |2020년 11월 20일|대전광역시 유성구|유석재|과학기술정보통신부 |한국핵융합에너지연구원 | |
  |국방과학연구소 |1970년 08월 06일|대전광역시 유성구| |대한민국 방위사업청|국방과학연구소 | |
  |한국표준과학연구원 |1975년 12월 24일|대전광역시 유성구 가정로 267 (가정동)| ||한국표준과학연구원 | |
  |한국지질자원연구원 |1948년 09월 13일|대전광역시 유성구 과학로 124(가정동 30)| |과학기술정보통신부 |한국지질자원연구원 | |
  |한국항공우주연구원 | |대전광역시 유성구 과학로 169-84 | ||http://www.kari.re.kr/| |
  |한국화학연구원 |1976년|대한민국 대전광역시 유성구 | ||한국화학연구원 | |
  |한국과학기술정보연구원 |2001년 01월 01일|대한민국 대전광역시 유성구 대학로 245<br>(본원) 대한민국 서울특별시 동대문구 회기로66(분원) |김재수|과학기술정보통신부 |한국과학기술정보연구원 | |
  |한국과학기술원 | |본부 대전광역시 유성구 대학로 291<br>서울캠퍼스 서울특별시 동대문구 회기로 85<br>문지캠퍼스 대전광역시 유성구 문지로 193<br>도곡캠퍼스 서울특별시 강남구 논현로28길 25| ||kaist.ac.kr | |
  |한국해양수산개발원 |1997년 04월 18일|부산광역시 영도구 해양로301번길 26|김종덕|경제인문사회연구회 |https://www.kmi.re.kr/| |
  |통일연구원 |1991년 04월 09일|서울특별시 서초구 반포대로 217 |고유환|경제인문사회연구회 |http://www.kinu.or.kr/| |
  |한국형사·법무정책연구원|1989년 03월 16일|서울특별시 서초구 태봉로 114|하태훈|경제인문사회연구회 |https://www.kic.re.kr/| |
  |한국과학기술연구원 |1966년 02월 10일|서울특별시 성북구 화랑로14길 5 (하월곡동)| |대한민국 과학기술정보통신부|한국과학기술연구원 | |
  |한국여성정책연구원 |1983년 04월 21일|서울특별시 은평구 진흥로 225| |경제인문사회연구회 |https://www.kwdi.re.kr/| |
  |한국행정연구원 |1976년|서울특별시 은평구 진흥로 235|안성호|경제인문사회연구회 |https://www.kipa.re.kr/| |
  |한국법제연구원 |1990년 07월 30일|세종특별자치시 국책연구원로 15|김계홍|경제인문사회연구회 |http://www.klri.re.kr/| |
  |국토연구원 |1978년 10월 04일|세종특별자치시 국책연구원로 5 |강현수|경제인문사회연구회 |http://www.krihs.re.kr/| |
  |한국개발연구원 |1971년 03월 11일|세종특별자치시 남세종로 263 |조동철|경제인문사회연구회 |http://www.kdi.re.kr| |
  |KDI 국제정책대학원 | |세종특별자치시 남세종로 263 (반곡동 203-40)| ||http://www.kdischool.ac.kr/| |
  |한국조세재정연구원 |1992년 07월 15일|세종특별자치시 시청대로 336 |김재진|경제인문사회연구회 |https://www.kipf.re.kr| |
  |과학기술정책연구원 |1999년 5월 |세종특별자치시 시청대로 370 |문미옥|경제인문사회연구회 |http://www.stepi.re.kr/| |
  |한국노동연구원 |1988년 08월 25일|세종특별자치시 시청대로 370 |배규식|경제인문사회연구회 |https://www.kli.re.kr/| |
  |한국직업능력연구원 |1997년 10월 18일|세종특별자치시 시청대로 370 사회정책동(D동) |류장수|경제인문사회연구회 |http://www.krivet.re.kr/| |
  |한국환경연구원 |1997년 09월 08일|세종특별자치시 시청대로 370 세종국책연구단지 B동(과학'인프라동 8층-11층) |윤제용|경제인문사회연구회 |http://www.kei.re.kr/| |
  |대외경제정책연구원 |1989년 12월|세종특별자치시 시청대로 370 세종국책연구단지 경제정책동|김흥종|경제인문사회연구회 |http://www.kiep.go.kr/| |
  |산업연구원 |1976년|세종특별자치시 시청대로 370 세종국책연구단지 경제정책동|장지상|경제인문사회연구회 |http://www.kiet.re.kr/| |
  |한국교통연구원 |1986년 2월 |세종특별자치시 시청대로 370 세종국책연구단지 과학인프라동 |오재학|경제인문사회연구회 |https://www.koti.re.kr/| |
  |한국청소년정책연구원|1989.07|세종특별자치시 시청대로 370 세종국책연구단지 사회정책동(D동)<br>한국청소년정책연구원 6/7층 |김현철|국무총리|https://www.nypi.re.kr/| |
  |한국보건사회연구원 |1981년 07월 01일|세종특별자치시 시청대로 370, 사회정책동 1~5층 |이태수|경제인문사회연구회 |https://www.kihasa.re.kr/| |
  |에너지경제연구원|1986년 09월 01일|울산광역시 중구 종가로 405-11|임춘택|경제인문사회연구회 |http://www.keei.re.kr/| |
  |한국농촌경제연구원 |1978년 04월 01일|전라남도 나주시 빛가람로 601|한두봉|경제인문사회연구회 |http://www.krei.re.kr/| |
  |한국식품연구원 | |전라북도 완주군 이서면 농생명로 245|백형희||http://www.kfri.re.kr/| |
  |국립생태원 | |충청남도 서천군 마서면 금강로 1210| ||http://www.nie.re.kr/| |
  |국립해양생물자원관 |2015년 04월 20일|충청남도 서천군 장항읍 장산로101번길 75 | |대한민국 해양수산부|http://www.mabik.re.kr/| |
  |한국교육개발원 |1972년 8월 |충청북도 진천군 덕산읍 교학로 7 |류방란|경제인문사회연구회 |www.kedi.re.kr/ | |
  |한국교육과정평가원 |1998년 01월 01일|충청북도 진천군 덕산읍 교학로 8 | |경제인문사회연구회 |http://www.kice.re.kr/| |
  |정보통신정책연구원 |1985년 02월 04일|충청북도 진천군 덕산읍 정통로 18|권호열|경제인문사회연구회 |http://www.kisdi.re.kr/| |
  |국립암센터 | | | |보건복지부 ||오류 |
  |건축공간연구원 | | | |||오류 |
  |육아정책연구소 | | | |||오류 |
  |녹색기술센터| | | |||오류 |
  |한국기초과학지원연구원 | | | |||오류 |
  |한국생명공학연구원 | | | |||오류 |
  |한국한의학연구원| | | |||오류 |
  |한국생산기술연구원 | | | |||오류 |
  |한국전자통신연구원 | | | |||오류 |
  |국가보안기술연구소 | | | |||오류 |
  |한국건설기술연구원 | | | |||오류 |
  |한국철도기술연구원 | | | |||오류 |
  |세계김치연구소 | | | |||오류 |
  |한국기계연구원 | | | |||오류 |
  |한국재료연구원 | | | |||오류 |
  |한국에너지기술연구원| | | |||오류 |
  |안전성평가연구소| | | |||오류 |
  |한국원자력연구원| | | |||오류 |
  |기초과학연구원 | | | |||오류 |
  |국가수리과학연구소 | | | |||오류 |
  |고등과학원 | | | |||오류 |
  |한국해양과학기술원 | | | |||오류 |
  |극지연구소 | | | |||오류 |
  |선박해양플랜트연구소| | | |||오류 |
  |한국국방연구원 | | | |||오류 |
  |국방기술품질원 | | | |||오류 |
  |한국학중앙연구원| | | |||오류 |
  |국립낙동강생물자원관| | | |||오류 |
  |원자력의학원| | | |||문서 없음|
  |한국과학재단| | | |||문서 없음|
  |원자력안전기술원| | | |||문서 없음|
  |국립호남권생물자원관| | | |||문서 없음|
  </details>