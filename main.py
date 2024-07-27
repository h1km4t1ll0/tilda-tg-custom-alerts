import os
import urllib.parse

from aiogram import Bot
from aiohttp import web
from aiohttp.abc import BaseRequest

routes = web.RouteTableDef()
bot = Bot(os.environ.get('BOT_TOKEN'))
form_id_map = {}

list_environ_keys = list(filter(lambda each: each.startswith('TILDA_FORM_'), os.environ.keys()))
for environ_key in list_environ_keys:
    form_id_map[environ_key.split('_')[-1]] = os.environ.get(environ_key)


@routes.post('/')
async def hello(request: BaseRequest):
    try:
        data = urllib.parse.parse_qs(urllib.parse.unquote((await request.content.read()).decode('utf-8')))
        print(data)
        chat_id = os.environ.get('CHAT_ID')
        await bot.send_message(
            chat_id,
            '<b>Новая заявка на сайте.</b>\n\n'
            f'<b>Имя</b>: {data['Name'][0]}\n'
            f'<b>Телефон</b>: +{"-".join(
                data['Phone'][0].split()
            ).replace('(', '').replace(')', '').replace('-', '')}\n'
            f'<b>Форма</b>: {form_id_map[data['formid'][0]]}\n',
            parse_mode='html'
        )
    except Exception as e:
        print('error', e)
    return web.Response(text='200')


app = web.Application()
app.add_routes(routes)
web.run_app(app, port=18390)
