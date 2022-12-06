from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Bot start'
        ),
        BotCommand(
            command='cancel',
            description='Cancel current action'
        ),
        BotCommand(
            command='lang',
            description='Change language'
        ),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
