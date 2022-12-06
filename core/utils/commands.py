from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram.utils.i18n import gettext as _


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description=_('Начало работы')
        ),
        BotCommand(
            command='cancel',
            description=_('Отменить действие')
        ),
        BotCommand(
            command='catalogue',
            description=_('Каталог')
        ),
        BotCommand(
            command='payment',
            description=_('Пополнить баланс')
        ),
        BotCommand(
            command='profile',
            description=_('Мой профиль')
        ),
        BotCommand(
            command='question',
            description=_('Задать вопрос')
        ),
        BotCommand(
            command='lang',
            description=_('Изменить язык')
        ),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
