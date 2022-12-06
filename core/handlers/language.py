from aiogram import Router
from aiogram.filters import Command
from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.utils.i18n import gettext as _
from core.middlewares.i18nmiddleware import DBI18nMiddleware
from core.keyboards.language import select_language


router = Router()


@router.message(Command(commands=["lang"]))
async def start_handler(message: Message):
    await message.answer(_('Выбери язык'), reply_markup=select_language)
    await message.delete()


@router.callback_query(F.data.startswith('set_lang'))
async def set_lang_ru(call: CallbackQuery, request: DBI18nMiddleware):
    lang = call.data.split()[0]
    await call.message.delete()
    if lang == 'ru':
        await request.set_locale(call.from_user.id, 'ru')
        await call.answer('Язык изменен')
    elif lang == 'en':
        await request.set_locale(call.from_user.id, 'en')
        await call.answer('Language set')
    else:
        await call.answer('Error')
