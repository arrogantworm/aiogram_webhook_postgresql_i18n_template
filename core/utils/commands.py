from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram.utils.i18n import lazy_gettext as __


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description=__('Начало работы')
        ),
        BotCommand(
            command='cancel',
            description=__('Отменить действие')
        ),
        BotCommand(
            command='catalogue',
            description=__('Каталог')
        ),
        BotCommand(
            command='payment',
            description=__('Пополнить баланс')
        ),
        BotCommand(
            command='profile',
            description=__('Мой профиль')
        ),
        BotCommand(
            command='question',
            description=__('Задать вопрос')
        ),
        BotCommand(
            command='lang',
            description=__('Изменить язык')
        ),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
