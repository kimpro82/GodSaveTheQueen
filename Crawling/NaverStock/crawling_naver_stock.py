"""
네이버 주식 종목게시판 크롤링
2023.06.10
"""


import asyncio
import pprint
import re
from bs4 import BeautifulSoup
import aiohttp


async def fetch(session, url):

    async with session.get(url) as response:
        return await response.text()


async def get_post(session, code, page):

    url = f"https://finance.naver.com/item/board.naver?code={code}&page={page}"
    time_list = []
    time_pattern = r"(\d{4})\.(\d{2})\.(\d{2}) (\d{2}):(\d{2})"

    html = await fetch(session, url)
    soup = BeautifulSoup(html, "html.parser")

    spans = soup.select(".section.inner_sub table tbody tr span")

    if TEST:
        print(url)                                                              # Ok
        # print(soup)                                                           # Ok
        # pprint.pprint(spans)                                                  # Ok

    for span in spans:
        match = re.search(time_pattern, span.text)
        if match:
            time_list.append(match.group())

    return code, page, time_list


async def main():

    if TEST:
        codes = ["005930"]
        pages = ["1"]
    else:
        codes = ["005930", "373220", "000660"]                                  # 삼성전자, LG에너지솔루션, SK하이닉스
        pages = ["1", "2", "3"]

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.115'}
    # headers = {'User-Agent': 'Edg/109.0.1518.115'}                            # doesn't work but don't know why
    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = []
        for code in codes:
            for page in pages:
                task = asyncio.create_task(get_post(session, code, page))
                tasks.append(await task)

        return tasks


if __name__ == "__main__":

    TEST = True
    loop = asyncio.get_event_loop()
    tasks = loop.run_until_complete(main())

    for task in tasks:
        code, page, time_list = task
        pprint.pprint(f"종목: {code}, 페이지: {page}, 게시일시: {time_list}")
