import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup

import os
os.environ['PYPPETEER_DOWNLOAD_HOST'] = 'https://npm.taobao.org/mirrors'
async def main():
    browser = await launch(headless=True,options={'args': ['--no-sandbox']})
    page = await browser.newPage()
    await page.goto('https://www.917500.cn/sdtgj/m/kjfb.html')

    content = await page.content()
    soup = BeautifulSoup(content, 'html.parser')

    # 获取id为'body'的body标签
    body = soup.find('tbody', id='body')

    # 获取body中的所有tr标签，并取最后一个
    last_tr = body.find_all('tr')[-1]

    # 获取last_tr中第二个class为'k1'的td标签
    second_td = last_tr.find_all('td', class_='k1')[1]
    # print(f'{second_td.text.split()}')
    # # 获取td标签中的文本，并将其分割成一个数组
    # values = [int(x) for x in second_td.text.split() if x.isdigit()]
    num_list = num_list =  [int(i) for i in str(second_td.text.split()[0])]

    print(f'{num_list}')

    await browser.close()

asyncio.get_event_loop().run_until_complete(main())