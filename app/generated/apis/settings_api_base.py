# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from app.generated.models.error import Error
from app.generated.models.printer import Printer
from app.generated.models.printer_input import PrinterInput
from app.generated.models.settings import Settings
from app.generated.models.settings_input import SettingsInput


class BaseSettingsApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseSettingsApi.subclasses = BaseSettingsApi.subclasses + (cls,)
    async def get_settings(
        self,
    ) -> Settings:
        ...


    async def update_settings(
        self,
        settings_input: SettingsInput,
    ) -> Settings:
        """Сад должен существовать."""
        ...


    async def set_printer(
        self,
        printer_input: PrinterInput,
    ) -> Printer:
        ...


    async def clear_printer(
        self,
    ) -> Printer:
        """Возвращает device: null."""
        ...
