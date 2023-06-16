"""
네이버 주식 종목게시판 크롤링 v0.1
2023.06.16

작성자: Your prince

기능:
    - 네이버 종목 게시판에서 일정한 종목, 페이지 범위의 게시물 게시일시 및 제목을 크롤링함.
    - 종목 및 페이지 범위는 임시로 main() 안에서 리스트로 지정
    - TEST 모드 지정 가능(True / False)

향후 개선점:
    - 더 많은 종목 리스트: ex. 코스피200, 상장사 전체 등
    - 더 많은 페이지 수: ex. 특정 기간까지, 혹은 마지막 페이지까지 등
    - 크롤링 항목 추가: 본문, 글쓴이 ID 등
"""


import asyncio
import pprint
import re
from bs4 import BeautifulSoup
import aiohttp


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


if __name__ == "__main__":

    TEST = False
    loop = asyncio.get_event_loop()
    tasks = loop.run_until_complete(main())

    for task in tasks:
        code, page, time_title_list = task
        for time_title in time_title_list:
            print(f"종목: {code}, 페이지: {page}, 게시일시: {time_title[0]}, 제목: {time_title[1]}")
