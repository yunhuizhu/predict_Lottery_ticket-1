import asyncio
from pyppeteer import launch

from bs4 import BeautifulSoup
import site
import os
os.environ['PYPPETEER_DOWNLOAD_HOST'] = 'https://npm.taobao.org/mirrors'
async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://tools.17500.cn/tb/gdfc36x7/hmfb?limit=400')

    content = await page.content()
    soup = BeautifulSoup(content, 'html.parser')

    tbody = soup.find('tbody', {'id': 'body'})
    trs = tbody.find_all('tr')
    trs.reverse()
    data = []
    for tr in trs:
        item = dict()
        tds = tr.find_all('td', {'class': 'bc'})
        if len(tds) == 2 and tds[0].text.isdigit():
            item[u"期数"] = tds[0].text.strip()
            numlist = tds[1].text.replace('|', ',').strip().split(",")
            # if name == "qxc":
            #     red_nums = 7
            # elif name in ["pls", "sd"]:
            #     red_nums = 3
            red_nums = len(numlist)
            for i in range(red_nums):
                item[u"红球_{}".format(i + 1)] = numlist[i]
            data.append(item)
            print(tds[0].text, tds[1].text.replace('|', ','))

    await browser.close()

asyncio.get_event_loop().run_until_complete(main())