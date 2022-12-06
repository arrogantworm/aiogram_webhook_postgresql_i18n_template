from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Начало работы'
        ),
        BotCommand(
            command='cancel',
            description='Отменить действие'
        ),
        BotCommand(
            command='catalogue',
            description='Каталог'
        ),
        BotCommand(
            command='payment',
            description='Пополнить баланс'
        ),
        BotCommand(
            command='profile',
            description='Мой профиль'
        ),
        BotCommand(
            command='question',
            description='Задать вопрос'
        ),
        BotCommand(
            command='lang',
            description='Изменить язык'
        ),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
