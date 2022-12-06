from aiogram.utils.i18n import I18nMiddleware, I18n
from aiogram.types import TelegramObject
from typing import Callable, Awaitable, Dict, Any
from core.utils.dbconnect import Request


class DBI18nMiddleware(I18nMiddleware):

    async def get_locale(self, event: TelegramObject, data: Dict[str, Any]) -> str:
        return await Request.get_locale(user_id=data['user_id'])
