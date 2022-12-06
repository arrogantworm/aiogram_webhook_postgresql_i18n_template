from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.methods import DeleteMyCommands
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.filters.text import Text
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __
from core.middlewares.i18nmiddleware import DBI18nMiddleware
from core.utils import dbconnect
from core.utils import commands


router = Router()


@router.message(Command(commands=["start"]))
async def start_handler(message: Message, state: FSMContext, request: dbconnect.Request):
    await request.new_user(message.from_user.id, message.from_user.username)
    await state.clear()
    await message.answer(_('Привет'), reply_markup=ReplyKeyboardRemove())


@router.message(Command(commands=["en"]))
async def start_handler(message: Message, request: DBI18nMiddleware, bot: Bot):
    await request.set_locale(message.from_user.id, 'en')
    await bot(DeleteMyCommands())
    await commands.set_commands_en(bot)
    await message.answer(_('Language set'), reply_markup=ReplyKeyboardRemove())


@router.message(Command(commands=["ru"]))
async def start_handler(message: Message, request: DBI18nMiddleware, bot: Bot):
    await request.set_locale(message.from_user.id, 'ru')
    await bot(DeleteMyCommands())
    await commands.set_commands_ru(bot)
    await message.answer(_('Язык изменен'), reply_markup=ReplyKeyboardRemove())


@router.message(Command(commands=["cancel"]))
@router.message(Text(text="отмена", ignore_case=True))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=ReplyKeyboardRemove()
    )
