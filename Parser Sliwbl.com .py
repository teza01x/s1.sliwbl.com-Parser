import asyncio
import aiohttp
from bs4 import BeautifulSoup
import time


page_count = int(input('По какую страницу ищем: '))
search_info = input('Поиск по совпадениям: ')
lessons_list = []

start = time.time()


def data_mining(resp_text):
    soup = BeautifulSoup(resp_text, 'lxml')
    objs = soup.findAll('div', class_='structItem-cell structItem-cell--main')
    for i in objs:
        name = i.find('div', class_='structItem-title').find('a', class_='').text.strip()
        link = i.find('div', class_='structItem-title').find('a', class_='').get('href')
        if search_info.casefold() in name.casefold():
            lessons_list.append({
                'Название': name,
                'Ссылка': link,
            })


async def get_page_data(session, path: str, id_page: int) -> str:
    if id_page:
        url = f'https://s1.sliwbl.com/forums/{path}/page-{id_page}'
    else:
        url = f'https://s1.sliwbl.com/forums/{path}/page-{id_page}'
    async with session.get(url) as resp:
        assert resp.status == 200
        # print(f'get url: {url}')
        resp_text = await resp.text()
        data_mining(resp_text)
        # return resp_text


async def find_lessons():
    forum_path = ['programmirovanie.27']
    async with aiohttp.ClientSession() as session:
        tasks = []
        for path in forum_path:
            for id_page in range(page_count):
                task = asyncio.create_task(get_page_data(session, path, id_page))
                tasks.append(task)
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(find_lessons())

    print(lessons_list)
    end = time.time()
    total_time = end - start
    print('Это заняло {} секунд что бы промониторить {} стр.'.format(total_time, page_count))