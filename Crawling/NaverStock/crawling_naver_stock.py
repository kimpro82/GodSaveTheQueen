"""
네이버 주식 종목게시판 크롤링
2023.06.10
"""


import asyncio
import pprint
import re
from bs4 import BeautifulSoup
import aiohttp


async def fetch(_session, _url):

    async with _session.get(_url) as _response:
        return await _response.text()


async def get_post(_session, _code, _page):

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
