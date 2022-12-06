from aiogram.utils.i18n import I18nMiddleware
from aiogram.types import TelegramObject, Message
from typing import Callable, Awaitable, Dict, Any
from core.utils.dbconnect import Request


class DBI18nMiddleware(I18nMiddleware):

    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]):
        data['user_id'] = event.from_user.id

    async def get_locale(self, event: TelegramObject, data: Dict[str, Any]) -> str:
        return await Request.get_locale(user_id=data['user_id'])
