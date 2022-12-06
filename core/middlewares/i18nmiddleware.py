from abc import ABC, abstractmethod
from typing import Any, Awaitable, Callable, Dict, Optional, Set, cast


try:
    from babel import Locale, UnknownLocaleError
except ImportError:  # pragma: no cover
    Locale = None

    class UnknownLocaleError(Exception):  # type: ignore
        pass


from aiogram import BaseMiddleware, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject, User
from aiogram.utils.i18n.core import I18n


class I18nMiddleware(BaseMiddleware, ABC):
    """
    Abstract I18n middleware.
    """

    def __init__(
        self,
        i18n: I18n,
        i18n_key: Optional[str] = "i18n",
        middleware_key: str = "i18n_middleware",
    ) -> None:
        """
        Create an instance of middleware

        :param i18n: instance of I18n
        :param i18n_key: context key for I18n instance
        :param middleware_key: context key for this middleware
        """
        self.i18n = i18n
        self.i18n_key = i18n_key
        self.middleware_key = middleware_key


    def setup(
        self: BaseMiddleware, router: Router, exclude: Optional[Set[str]] = None
    ) -> BaseMiddleware:
        """
        Register middleware for all events in the Router

        :param router:
        :param exclude:
        :return:
        """
        if exclude is None:
            exclude = set()
        exclude_events = {"update", *exclude}
        for event_name, observer in router.observers.items():
            if event_name in exclude_events:
                continue
            observer.outer_middleware(self)
        return self


class SimpleI18nMiddleware(I18nMiddleware):
    """
    Simple I18n middleware.

    Chooses language code from the User object received in event
    """

    def __init__(
        self,
        i18n: I18n,
        i18n_key: Optional[str] = "i18n",
        middleware_key: str = "i18n_middleware",
    ) -> None:
        super().__init__(i18n=i18n, i18n_key=i18n_key, middleware_key=middleware_key)

        if Locale is None:  # pragma: no cover
            raise RuntimeError(
                f"{type(self).__name__} can be used only when Babel installed\n"
                "Just install Babel (`pip install Babel`) "
                "or aiogram with i18n support (`pip install aiogram[i18n]`)"
            )

    async def get_locale(self, event: TelegramObject, data: Dict[str, Any]) -> str:
        if Locale is None:  # pragma: no cover
            raise RuntimeError(
                f"{type(self).__name__} can be used only when Babel installed\n"
                "Just install Babel (`pip install Babel`) "
                "or aiogram with i18n support (`pip install aiogram[i18n]`)"
            )

        event_from_user: Optional[User] = data.get("event_from_user", None)
        if event_from_user is None or event_from_user.language_code is None:
            return self.i18n.default_locale
        try:
            locale = Locale.parse(event_from_user.language_code, sep="-")
        except UnknownLocaleError:
            return self.i18n.default_locale

        if locale.language not in self.i18n.available_locales:
            return self.i18n.default_locale
        return cast(str, locale.language)
