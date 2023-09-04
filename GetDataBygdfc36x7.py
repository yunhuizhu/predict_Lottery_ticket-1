import asyncio
from pyppeteer import launch
import os
os.environ['PYPPETEER_DOWNLOAD_HOST'] = 'https://npm.taobao.org/mirrors'

async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://tools.17500.cn/tb/gdfc36x7/hmfb')
    await asyncio.sleep(20)  # 等待JS执行完毕

    elements = await page.querySelectorAll('#body tbody tr')  # 获取所有tr元素
    for element in reversed(elements):  # 从后往前遍历
        tds = await element.querySelectorAll('td.bc')  # 获取class为bc的td元素
        if len(tds) == 2:  # 如果有两个td元素
            first_td_value = await (await tds[0].getProperty('textContent')).jsonValue()  # 获取第一个td元素的值
            if first_td_value.isdigit():  # 如果第一个td元素的值是数字
                second_td_value = await (await tds[1].getProperty('textContent')).jsonValue()  # 获取第二个td元素的值
                red_ball = second_td_value.replace('|', ',')  # 把|替换成逗号
                print(f"序号：{first_td_value}, 红球：{red_ball}")  # 打印结果

    await browser.close()

asyncio.get_event_loop().run_until_complete(main())