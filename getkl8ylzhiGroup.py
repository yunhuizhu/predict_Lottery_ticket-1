import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup

async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://www.917500.cn/kt8/yl/100.html')

    content = await page.content()
    soup = BeautifulSoup(content, 'html.parser')

    tr = soup.find('tr', id='bott_yc_1')
    numbers = [[] for _ in range(10)]

    if tr:
        for td in tr.find_all('td'):
            for i in range(10):
                if f'fqn-{i+1}' in td.get('class', []):
                    numbers[i].append(int(td.text))

    for i, nums in enumerate(numbers):
        print(f'yl_fqn_{i+1}=', nums)

    await browser.close()

asyncio.get_event_loop().run_until_complete(main())