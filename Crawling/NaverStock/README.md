# [Stock Bulletin Board in Naver](../../README.md#web-crawling)

My wife can't live without me


### \<List>

- [Stock Bulletin Board in Naver v0.1 (2023.06.16)](#stock-bulletin-board-in-naver-v01-20230616)


## [Stock Bulletin Board in Naver v0.1 (2023.06.16)](#list)

- 작성자: Your prince

- 기능:
  - 네이버 종목 게시판에서 일정한 종목, 페이지 범위의 게시물 게시일시 및 제목을 크롤링
  - 종목 및 페이지 범위는 임시로 `main()` 안에서 리스트로 지정
  - TEST 모드 지정 가능(`True` / `False`)

- 향후 개선점:
  - 크롤링 항목 추가: 본문, 글쓴이 ID 등
  - 크롤링 결과의 별도 파일 저장
  - 더 많은 종목 리스트: ex. 코스피200, 상장사 전체 등
  - 더 많은 페이지 수: ex. 특정 기간까지, 혹은 마지막 페이지까지 등
  - 크롤링 양이 많아질 시 진행률 표시

- 기타:
  - `Redefining name 'xxxxxx' from outer scope` 에러에 대응하기 위해 함수내 변수명 앞에 모두 `_`를 붙였는데 잘 한 건지 모르겠음
  - 속도 통제 필요한지 검토 필요 (현재 별도 딜레이 부과없이 비동기 방식으로 구현)

  <br><details>
    <summary>Codes : crawling_naver_stock.py</summary>

  ```py
  import asyncio
  import pprint
  import re
  from bs4 import BeautifulSoup
  import aiohttp
  ```
  ```py
  async def fetch(_session, _url):
      """
      지정된 URL에서 HTML 데이터를 가져옵니다.

      Args:
          _session: aiohttp 클라이언트 세션 객체
          _url: 가져올 URL

      Returns:
          _response의 텍스트 데이터
      """
      async with _session.get(_url) as _response:
          return await _response.text()
  ```
  ```py
  async def get_post(_session, _code, _page):
      """
      종목 코드와 페이지 번호에 해당하는 주식 종목게시판 데이터를 가져옵니다.

      Args:
          _session: aiohttp 클라이언트 세션 객체
          _code: 종목 코드
          _page: 페이지 번호

      Returns:
          _code, _page, 게시일시와 제목으로 구성된 리스트
      """
      _url = f"https://finance.naver.com/item/board.naver?code={_code}&page={_page}"
      _time_list = []
      _title_list = []

      _html = await fetch(_session, _url)
      _soup = BeautifulSoup(_html, "html.parser")
      _spans1 = _soup.select(".section.inner_sub table tbody tr td span")
      _spans2 = _soup.select(".section.inner_sub table tbody tr td[class='title'] a")

      if TEST:
          print(_url)                                                             # Ok
          # print(_soup)                                                          # Ok
          pprint.pprint(_spans2)

      _time_pattern = r"(\d{4})\.(\d{2})\.(\d{2}) (\d{2}):(\d{2})"
      for _span in _spans1:
          _match = re.search(_time_pattern, _span.text)
          if _match:
              _time_list.append(_match.group())

      for _span in _spans2:
          _title_list.append(_span['title'])

      _time_title_list = list(zip(_time_list, _title_list))

      return _code, _page, _time_title_list
  ```
  ```py
  async def main():
      """
      메인 함수입니다. 비동기로 주식 종목게시판 데이터를 가져와 출력합니다.

      Returns:
          _tasks의 비동기 결과 리스트
      """
      if TEST:
          _codes = ["005930"]
          _pages = ["1"]
      else:
          _codes = ["005930", "373220", "000660"]                                 # 삼성전자, LG에너지솔루션, SK하이닉스
          _pages = ["1", "2", "3"]

      _headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.115'}
      # _headers = {'User-Agent': 'Edg/109.0.1518.115'}                           # doesn't work but don't know why
      async with aiohttp.ClientSession(headers=_headers) as _session:
          _tasks = []
          for _code in _codes:
              for _page in _pages:
                  _task = asyncio.create_task(get_post(_session, _code, _page))
                  _tasks.append(await _task)

          return _tasks
  ```
  ```py
  if __name__ == "__main__":

      TEST = False
      loop = asyncio.get_event_loop()
      tasks = loop.run_until_complete(main())

      for task in tasks:
          code, page, time_title_list = task
          for time_title in time_title_list:
              print(f"종목: {code}, 페이지: {page}, 게시일시: {time_title[0]}, 제목: {time_title[1]}")
    ```

  </details>
  <details open>
    <summary>Output (Console)</summary>

  ```text
  종목: 005930, 페이지: 1, 게시일시: 2023.06.16 14:37, 제목: 후쿠시마 괴담에 소금 사재기 한 그 바보들
  종목: 005930, 페이지: 1, 게시일시: 2023.06.16 14:37, 제목: ●왜놈 윤재앙 지지층 토착왜구 사이비 집단
  종목: 005930, 페이지: 1, 게시일시: 2023.06.16 14:36, 제목: 하루. 좽일
  종목: 005930, 페이지: 1, 게시일시: 2023.06.16 14:36, 제목: 8만원을 찍고 있어도 부족한데...
  종목: 005930, 페이지: 1, 게시일시: 2023.06.16 14:36, 제목: 다음주를 위해 미리 알고 계셔야 할 내용
  ……
  ```
  Crazy
  </details>
