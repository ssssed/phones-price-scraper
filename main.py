import json

from bs4 import BeautifulSoup
import asyncio
import aiohttp


pages = [
    'https://www.itsworthmore.com/sell/iphone',
    'https://www.itsworthmore.com/sell/galaxy-z-fold-series',
    'https://www.itsworthmore.com/sell/galaxy-s-series',
    'https://www.itsworthmore.com/sell/galaxy-note-series'
]

async def get_page_data(session, page):
    headers = {}
    result_data = []
    page_name = page.split('/')[-1]
    async with session.get(url=page, headers=headers, ssl=False) as response:
        response_text = await response.text()
        soup = BeautifulSoup(response_text, 'lxml')
        phone_cards = soup.find('ul',
                                class_=['small-block-grid-2', 'medium-block-grid-3', 'large-block-grid-4']).findAll(
            'li')
        for card in phone_cards:
            card_img = card.findNext('img').get('src')
            card_name = card.findNext('a').text.strip().split('\n')[0]
            card_price = card.findNext('strong').text
            result_data.append({
                "img": card_img,
                "name": card_name,
                "price": card_price
            })
        with open(f'data/{page_name}.json', 'w') as file:
            json.dump(result_data, file, indent=4, ensure_ascii=False)

async def gather_data():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for page in pages:
            task = asyncio.create_task(get_page_data(session, page))
            tasks.append(task)

        await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(gather_data())