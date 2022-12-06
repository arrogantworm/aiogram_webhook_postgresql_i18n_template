from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import any_state
from aiogram.utils.i18n import FSMI18nMiddleware
from aiogram.filters.text import Text
from aiogram.utils.i18n import gettext as _
from core.utils import dbconnect


router = Router()


@router.message(Command(commands=["start"]))
async def start_handler(message: Message, state: FSMContext, request: dbconnect.Request):
    await request.new_user(message.from_user.id, message.from_user.username)
    await state.clear()
    await message.answer(_('Привет'), reply_markup=ReplyKeyboardRemove())


@router.message(Command(commands=["en"]))
async def start_handler(message: Message, state: FSMContext):
    await FSMI18nMiddleware.set_locale(state=state, locale='en')
    await message.answer(_('Привет'), reply_markup=ReplyKeyboardRemove())


@router.message(Command(commands=["ru"]))
async def start_handler(message: Message, state: FSMContext):
    await FSMI18nMiddleware.set_locale(state=state, locale='ru')
    await message.answer(_('Привет'), reply_markup=ReplyKeyboardRemove())


@router.message(Command(commands=["cancel"]))
@router.message(Text(text="отмена", ignore_case=True))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=ReplyKeyboardRemove()
    )
