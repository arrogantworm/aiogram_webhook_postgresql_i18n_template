from aiogram.utils.i18n import SimpleI18nMiddleware
from typing import Any, Dict, Optional, cast
from core.utils.dbconnect import Request
from aiogram.types import TelegramObject, User
from aiogram.utils.i18n.core import I18n


class DBI18nMiddleware(SimpleI18nMiddleware):

    def __init__(
        self,
        i18n: I18n,
        key: str = "locale",
        i18n_key: Optional[str] = "i18n",
        middleware_key: str = "i18n_middleware",
    ) -> None:
        super().__init__(i18n=i18n, i18n_key=i18n_key, middleware_key=middleware_key)
        self.key = key

    async def get_locale(self, event: TelegramObject, data: Dict[str, Any]) -> str:
        event_from_user: Optional[User] = data.get("event_from_user", None)
        if event_from_user is None or event_from_user.id is None:
            return self.i18n.default_locale
        try:
            locale = Request.get_locale(event_from_user.id)
            print(locale)
        except:
            return self.i18n.default_locale
        if locale not in self.i18n.available_locales:
            return self.i18n.default_locale
        return cast(str, locale)

    async def set_locale(self, user_id: int, locale: str) -> None:
        await Request.set_locale(user_id, locale)
        self.i18n.current_locale = locale
