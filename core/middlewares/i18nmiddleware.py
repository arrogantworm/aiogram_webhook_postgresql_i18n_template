import asyncpg
from aiogram.utils.i18n import SimpleI18nMiddleware
from typing import Any, Dict, Optional, cast, Callable, Awaitable
from core.utils.dbconnect import Request
from aiogram.types import TelegramObject, User, Message
from aiogram.utils.i18n import I18n
from core.middlewares.dbmiddleware import DbSession


class DBI18nMiddleware(SimpleI18nMiddleware):

    def __init__(
        self,
        connector: asyncpg.pool.Pool,
        i18n: I18n,
        key: str = "locale",
        i18n_key: Optional[str] = "i18n",
        middleware_key: str = "i18n_middleware",
    ) -> None:
        super().__init__(i18n=i18n, i18n_key=i18n_key, middleware_key=middleware_key)
        self.key = key
        self.connector = connector

    async def __call__(self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        async with self.connector.acquire() as connect:
            data['request'] = Request(connect)
            return await handler(event, data)

    async def get_locale(self, event: TelegramObject, data: Dict[str, Any]) -> str:
        event_from_user: Optional[User] = data.get("event_from_user", None)
        if event_from_user is None or event_from_user.id is None:
            return self.i18n.default_locale
        try:
            locale = self.sql_get_locale(event_from_user.id)
        except:
            return self.i18n.default_locale
        if locale not in self.i18n.available_locales:
            return self.i18n.default_locale
        return cast(str, locale)

    async def set_locale(self, message: Message, locale: str) -> None:
        await self.sql_set_locale(message.from_user.id, locale)
        self.i18n.current_locale = locale


    async def sql_get_locale(self, user_id):
        query = """SELECT locale FROM UserInfo WHERE user_id = $1"""
        locale = await self.connector.fetchrow(query, user_id)
        return locale['locale']

    async def sql_set_locale(self, user_id, locale):
        query = """UPDATE UserInfo SET locale=$2 WHERE user_id = $1"""
        await self.connector.execute(query, user_id, locale)