import asyncpg
from aiogram.utils.i18n import I18nMiddleware
from typing import Any, Dict, Optional, cast, Callable, Awaitable
from core.utils.dbconnect import Request
from aiogram.types import TelegramObject, User, Message
from aiogram.utils.i18n.core import I18n


class DBI18nMiddleware(I18nMiddleware):

    def __init__(self,
                 i18n: I18n,
                 connector: asyncpg.pool.Pool):
        super().__init__(i18n=i18n)
        self.connector = connector

    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        async with self.connector.acquire() as connect:
            data['request'] = Request(connect)
            return await handler(event, data)

    async def get_locale(self, event: TelegramObject, data: Dict[str, Any]) -> str:
        event_from_user: Optional[User] = data.get("event_from_user", None)
        query = """SELECT locale FROM UserInfo WHERE user_id = $1"""
        locale = await self.connector.fetchrow(query, event_from_user.id)
        return locale

    async def set_locale(self, message: Message, locale: str) -> None:
        query = """UPDATE UserInfo SET locale=$2 WHERE user_id = $1"""
        await self.connector.execute(query, message.from_user.id, locale)
        self.i18n.current_locale = locale
