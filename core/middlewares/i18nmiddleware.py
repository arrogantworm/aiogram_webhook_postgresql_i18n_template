import asyncpg
from aiogram.utils.i18n.middleware import I18nMiddleware
from typing import Any, Dict, Optional, cast, Callable, Awaitable
from core.utils.dbconnect import Request
from aiogram.types import TelegramObject, User, Message
from aiogram.utils.i18n.core import I18n


class DBI18nMiddleware(I18nMiddleware):

    def __init__(
            self,
            i18n: I18n,
            connector: asyncpg.pool.Pool,
            key: str = "locale",
            i18n_key: Optional[str] = "i18n",
            middleware_key: str = "i18n_middleware",
    ) -> None:
        super().__init__(i18n=i18n, i18n_key=i18n_key, middleware_key=middleware_key)
        self.connector = connector
        self.key = key

    async def get_locale(self, event: TelegramObject, data: Dict[str, Any]) -> str:
        event_from_user: Optional[User] = data.get("event_from_user", None)
        if event_from_user is None or event_from_user.language_code is None:
            return self.i18n.default_locale
        user_id = event_from_user.id
        print(user_id)
        query = """SELECT locale FROM UserInfo WHERE user_id = $1"""
        locale = await self.connector.fetchrow(query, user_id)
        return locale

    async def set_locale(self, user_id: int, locale: str) -> None:
        query = """UPDATE UserInfo SET locale=$2 WHERE user_id = $1"""
        await self.connector.execute(query, user_id, locale)
        self.i18n.current_locale = locale
