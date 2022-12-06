from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands_ru(bot: Bot):
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


async def set_commands_en(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Bot start'
        ),
        BotCommand(
            command='cancel',
            description='Cancel'
        ),
        BotCommand(
            command='catalogue',
            description='Catalogue'
        ),
        BotCommand(
            command='payment',
            description='Payment'
        ),
        BotCommand(
            command='profile',
            description='My profile'
        ),
        BotCommand(
            command='question',
            description='Support ticket'
        ),
        BotCommand(
            command='lang',
            description='Change language'
        ),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())