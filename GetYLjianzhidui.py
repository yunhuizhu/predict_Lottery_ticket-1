import asyncio
from pyppeteer import launch
import pandas as pd
import os

os.environ['PYPPETEER_DOWNLOAD_HOST'] = 'https://npm.taobao.org/mirrors'

async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://www.917500.cn/tools/zhcx/num/all/dtype/2/ball/03,11,20,21,22,27,49,52,54,57,72,78.html')
    await asyncio.sleep(20)  # 等待JS执行完毕

    table = await page.querySelector('.sortable')  # 获取class="sortable"的table
    thead = await table.querySelector('thead')  # 获取thead标签
    tbody = await table.querySelector('tbody')  # 获取tbody标签

    # 获取标题
    head_tr = await thead.querySelector('tr')
    head_tds = await head_tr.querySelectorAll('td')
    titles = []
    for i in range(13):
        title = await (await head_tds[i].getProperty('textContent')).jsonValue()
        titles.append(title)

    # 获取列表内容
    body_trs = await tbody.querySelectorAll('tr')
    data = []
    for tr in body_trs:
        tds = await tr.querySelectorAll('td')
        row = []
        for i in range(13):
            value = await (await tds[i].getProperty('textContent')).jsonValue()
            row.append(value)
        data.append(row)

    await browser.close()

    # 导出到Excel
    df = pd.DataFrame(data, columns=titles)
    df.to_excel('xml/1116_leng_2.xlsx', index=False)

asyncio.get_event_loop().run_until_complete(main())