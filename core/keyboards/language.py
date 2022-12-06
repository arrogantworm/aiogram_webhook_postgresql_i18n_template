from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


select_language = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Русский',
            callback_data='set_lang ru'
        )
    ],
    [
        InlineKeyboardButton(
            text='English',
            callback_data='set_lang en'
        )
    ],
])
