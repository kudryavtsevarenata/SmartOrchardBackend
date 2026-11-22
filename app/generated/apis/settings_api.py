# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from app.generated.apis.settings_api_base import BaseSettingsApi
import app.impl

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    HTTPException,
    Path,
    Query,
    Response,
    Security,
    status,
)

from app.generated.models.error import Error
from app.generated.models.printer import Printer
from app.generated.models.printer_input import PrinterInput
from app.generated.models.settings import Settings
from app.generated.models.settings_input import SettingsInput

router = APIRouter()

ns_pkg = app.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/settings",
    responses={
        200: {"model": Settings, "description": "Успешный ответ"},
        500: {"model": Error, "description": "Внутренняя ошибка сервера."},
    },
    tags=["settings"],
    summary="Получить настройки",
    response_model_by_alias=True,
)
async def get_settings(
) -> Settings:
    if not BaseSettingsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseSettingsApi.subclasses[0]().get_settings()


@router.patch(
    "/settings",
    responses={
        200: {"model": Settings, "description": "Успешный ответ"},
        422: {"model": Error, "description": "VALIDATION_ERROR - ошибка валидации."},
        500: {"model": Error, "description": "Внутренняя ошибка сервера."},
    },
    tags=["settings"],
    summary="Обновить текущий сад",
    response_model_by_alias=True,
)
async def update_settings(
    settings_input: SettingsInput = Body(..., description=""),
) -> Settings:
    """Сад должен существовать."""
    if not BaseSettingsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseSettingsApi.subclasses[0]().update_settings(settings_input)


@router.put(
    "/settings/printer",
    responses={
        200: {"model": Printer, "description": "Успешный ответ"},
        422: {"model": Error, "description": "VALIDATION_ERROR - ошибка валидации."},
        500: {"model": Error, "description": "Внутренняя ошибка сервера."},
    },
    tags=["settings"],
    summary="Подключить принтер",
    response_model_by_alias=True,
)
async def set_printer(
    printer_input: PrinterInput = Body(..., description=""),
) -> Printer:
    if not BaseSettingsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseSettingsApi.subclasses[0]().set_printer(printer_input)


@router.delete(
    "/settings/printer",
    responses={
        200: {"model": Printer, "description": "Успешный ответ"},
        500: {"model": Error, "description": "Внутренняя ошибка сервера."},
    },
    tags=["settings"],
    summary="Отключить принтер",
    response_model_by_alias=True,
)
async def clear_printer(
) -> Printer:
    """Возвращает device: null."""
    if not BaseSettingsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseSettingsApi.subclasses[0]().clear_printer()
