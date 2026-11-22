# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from app.generated.apis.gardens_api_base import BaseGardensApi
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

from typing import Any, List
from uuid import UUID
from app.generated.models.error import Error
from app.generated.models.finance import Finance
from app.generated.models.garden import Garden
from app.generated.models.garden_input import GardenInput

router = APIRouter()

ns_pkg = app.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/gardens",
    responses={
        200: {"model": List[Garden], "description": "Успешный ответ"},
        500: {"model": Error, "description": "Внутренняя ошибка сервера."},
    },
    tags=["gardens"],
    summary="Список садов",
    response_model_by_alias=True,
)
async def list_gardens(
) -> List[Garden]:
    if not BaseGardensApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseGardensApi.subclasses[0]().list_gardens()


@router.post(
    "/gardens",
    status_code=201,
    responses={
        201: {"model": Garden, "description": "Запись создана"},
        422: {"model": Error, "description": "VALIDATION_ERROR - ошибка валидации."},
        500: {"model": Error, "description": "Внутренняя ошибка сервера."},
    },
    tags=["gardens"],
    summary="Создать сад",
    response_model_by_alias=True,
)
async def create_garden(
    garden_input: GardenInput = Body(..., description=""),
) -> Garden:
    """Культура должна существовать. Число деревьев &#x3D; floor(area_ha × 10000 / (row_spacing × tree_spacing)), от 1 до 10000. Ряды и места нумеруются с 1. Максимум 100 рядов. Начальный статус UNKNOWN."""
    if not BaseGardensApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseGardensApi.subclasses[0]().create_garden(garden_input)


@router.get(
    "/gardens/{garden_id}",
    responses={
        200: {"model": Garden, "description": "Успешный ответ"},
        404: {"model": Error, "description": "NOT_FOUND - ресурс не найден."},
        500: {"model": Error, "description": "Внутренняя ошибка сервера."},
    },
    tags=["gardens"],
    summary="Получить сад",
    response_model_by_alias=True,
)
async def get_garden(
    garden_id: UUID = Path(..., description=""),
) -> Garden:
    if not BaseGardensApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseGardensApi.subclasses[0]().get_garden(garden_id)


@router.delete(
    "/gardens/{garden_id}",
    status_code=204,
    response_model=None,
    responses={
        204: {"description": "Запись удалена"},
        404: {"model": Error, "description": "NOT_FOUND - ресурс не найден."},
        500: {"model": Error, "description": "Внутренняя ошибка сервера."},
    },
    tags=["gardens"],
    summary="Удалить сад",
    response_model_by_alias=True,
)
async def delete_garden(
    garden_id: UUID = Path(..., description=""),
) -> None:
    """Удаляет также деревья, зоны, расписания, затраты, осмотры и заметки сада."""
    if not BaseGardensApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseGardensApi.subclasses[0]().delete_garden(garden_id)


@router.patch(
    "/gardens/{garden_id}/finance",
    responses={
        200: {"model": Finance, "description": "Успешный ответ"},
        404: {"model": Error, "description": "NOT_FOUND - ресурс не найден."},
        422: {"model": Error, "description": "VALIDATION_ERROR - ошибка валидации."},
        500: {"model": Error, "description": "Внутренняя ошибка сервера."},
    },
    tags=["gardens"],
    summary="Обновить финансы сада",
    response_model_by_alias=True,
)
async def update_finance(
    garden_id: UUID = Path(..., description=""),
    finance: Finance = Body(..., description=""),
) -> Finance:
    if not BaseGardensApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseGardensApi.subclasses[0]().update_finance(garden_id, finance)
