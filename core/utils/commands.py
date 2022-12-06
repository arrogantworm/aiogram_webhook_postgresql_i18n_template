from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='menu',
            description='Show bot menu'
        ),
        BotCommand(
            command='cancel',
            description='Cancel current action'
        ),
        BotCommand(
            command='catalogue',
            description='Show catalogue'
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