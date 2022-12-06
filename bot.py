import asyncio
import asyncpg
import logging
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from aiogram.utils.i18n import I18n
from aiogram.utils.i18n.middleware import FSMI18nMiddleware
from aiogram.fsm.state import any_state
from aiogram.filters import Command
from core.settings import config
from core.utils import commands
from core.middlewares import dbmiddleware
from core.handlers import basic


async def on_startup(bot: Bot):
    await commands.set_commands(bot)
    await bot.send_message(chat_id=config.ADMIN_ID, text='Бот запущен')


async def on_shutdown(bot: Bot):
    await bot.send_message(chat_id=config.ADMIN_ID, text='Бот остановлен')


async def start():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - [%(levelname)s] - %(name)s - '
                               '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s')
    bot = Bot(config.BOT_TOKEN.get_secret_value())

    #i18n
    i18n = I18n(path="locales", default_locale="en", domain="messages")

    # PostgreSQL connection
    pool_connect = await asyncpg.create_pool(user=config.DB_USER.get_secret_value(),
                                             password=config.DB_PASSWORD.get_secret_value(),
                                             database=config.DB_NAME.get_secret_value(),
                                             host=config.DB_HOST,
                                             port=config.DB_PORT,
                                             command_timeout=60)

    # Dispatcher
    dp = Dispatcher()
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # Middlewares
    dp.update.middleware.register(FSMI18nMiddleware(i18n=i18n))
    dp.update.middleware.register(dbmiddleware.DbSession(pool_connect))

    # Routers
    dp.include_router(basic.router)

    try:
        await bot.set_webhook(
            url=config.URL_DOMAIN + config.URL_PATH,
            drop_pending_updates=True,
            allowed_updates=dp.resolve_used_update_types()
        )
        app = web.Application()
        SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=config.URL_PATH)
        setup_application(app, dp, bot=bot)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, host=config.SERVER_HOST, port=config.SERVER_PORT)
        await site.start()
        await asyncio.Event().wait()
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
