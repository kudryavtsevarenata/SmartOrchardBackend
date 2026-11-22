# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from app.generated.apis.zones_api_base import BaseZonesApi
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
from app.generated.models.zone import Zone
from app.generated.models.zone_input import ZoneInput

router = APIRouter()

ns_pkg = app.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/gardens/{garden_id}/zones",
    responses={
        200: {"model": List[Zone], "description": "Успешный ответ"},
        404: {"model": Error, "description": "NOT_FOUND - ресурс не найден."},
        500: {"model": Error, "description": "Внутренняя ошибка сервера."},
    },
    tags=["zones"],
    summary="Список зон сада",
    response_model_by_alias=True,
)
async def list_zones(
    garden_id: UUID = Path(..., description=""),
) -> List[Zone]:
    if not BaseZonesApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseZonesApi.subclasses[0]().list_zones(garden_id)


@router.post(
    "/gardens/{garden_id}/zones",
    status_code=201,
    responses={
        201: {"model": Zone, "description": "Запись создана"},
        404: {"model": Error, "description": "NOT_FOUND - ресурс не найден."},
        409: {"model": Error, "description": "DUPLICATE - имя зоны занято; CONFLICT - дерево входит в другую зону."},
        422: {"model": Error, "description": "VALIDATION_ERROR - ошибка валидации."},
        500: {"model": Error, "description": "Внутренняя ошибка сервера."},
    },
    tags=["zones"],
    summary="Создать зону",
    response_model_by_alias=True,
)
async def create_zone(
    garden_id: UUID = Path(..., description=""),
    zone_input: ZoneInput = Body(..., description=""),
) -> Zone:
    """Все деревья принадлежат данному саду."""
    if not BaseZonesApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseZonesApi.subclasses[0]().create_zone(garden_id, zone_input)


@router.get(
    "/gardens/{garden_id}/zones/{zone_id}",
    responses={
        200: {"model": Zone, "description": "Успешный ответ"},
        404: {"model": Error, "description": "NOT_FOUND - ресурс не найден."},
        500: {"model": Error, "description": "Внутренняя ошибка сервера."},
    },
    tags=["zones"],
    summary="Получить зону",
    response_model_by_alias=True,
)
async def get_zone(
    garden_id: UUID = Path(..., description=""),
    zone_id: UUID = Path(..., description=""),
) -> Zone:
    if not BaseZonesApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseZonesApi.subclasses[0]().get_zone(garden_id, zone_id)


@router.put(
    "/gardens/{garden_id}/zones/{zone_id}",
    responses={
        200: {"model": Zone, "description": "Успешный ответ"},
        404: {"model": Error, "description": "NOT_FOUND - ресурс не найден."},
        409: {"model": Error, "description": "DUPLICATE - имя зоны занято; CONFLICT - дерево входит в другую зону."},
        422: {"model": Error, "description": "VALIDATION_ERROR - ошибка валидации."},
        500: {"model": Error, "description": "Внутренняя ошибка сервера."},
    },
    tags=["zones"],
    summary="Обновить зону",
    response_model_by_alias=True,
)
async def update_zone(
    garden_id: UUID = Path(..., description=""),
    zone_id: UUID = Path(..., description=""),
    zone_input: ZoneInput = Body(..., description=""),
) -> Zone:
    """Все деревья принадлежат данному саду."""
    if not BaseZonesApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseZonesApi.subclasses[0]().update_zone(garden_id, zone_id, zone_input)


@router.delete(
    "/gardens/{garden_id}/zones/{zone_id}",
    status_code=204,
    response_model=None,
    responses={
        204: {"description": "Запись удалена"},
        404: {"model": Error, "description": "NOT_FOUND - ресурс не найден."},
        500: {"model": Error, "description": "Внутренняя ошибка сервера."},
    },
    tags=["zones"],
    summary="Удалить зону",
    response_model_by_alias=True,
)
async def delete_zone(
    garden_id: UUID = Path(..., description=""),
    zone_id: UUID = Path(..., description=""),
) -> None:
    """Удаляет расписания зоны."""
    if not BaseZonesApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseZonesApi.subclasses[0]().delete_zone(garden_id, zone_id)
