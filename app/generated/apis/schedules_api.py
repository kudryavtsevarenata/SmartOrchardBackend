# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from app.generated.apis.schedules_api_base import BaseSchedulesApi
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

from datetime import date
from pydantic import Field
from typing import Any, List, Optional
from typing_extensions import Annotated
from uuid import UUID
from app.generated.models.error import Error
from app.generated.models.schedule import Schedule
from app.generated.models.schedule_input import ScheduleInput

router = APIRouter()

ns_pkg = app.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/gardens/{garden_id}/schedules",
    responses={
        200: {"model": List[Schedule], "description": "Успешный ответ"},
        404: {"model": Error, "description": "NOT_FOUND - ресурс не найден."},
        500: {"model": Error, "description": "Внутренняя ошибка сервера."},
    },
    tags=["schedules"],
    summary="Список расписаний сада",
    response_model_by_alias=True,
)
async def list_schedules(
    garden_id: UUID = Path(..., description=""),
    zone_id: Annotated[Optional[UUID], Field(description="Зона полива")] = Query(None, description="Зона полива", alias="zone_id"),
    var_date: Annotated[Optional[date], Field(description="Интервалы, пересекающие этот день")] = Query(None, description="Интервалы, пересекающие этот день", alias="date"),
) -> List[Schedule]:
    """Сортировка по start."""
    if not BaseSchedulesApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseSchedulesApi.subclasses[0]().list_schedules(garden_id, zone_id, var_date)


@router.post(
    "/gardens/{garden_id}/schedules",
    status_code=201,
    responses={
        201: {"model": Schedule, "description": "Запись создана"},
        404: {"model": Error, "description": "NOT_FOUND - ресурс не найден."},
        409: {"model": Error, "description": "CONFLICT - пересечение интервалов одной зоны."},
        422: {"model": Error, "description": "VALIDATION_ERROR - ошибка валидации."},
        500: {"model": Error, "description": "Внутренняя ошибка сервера."},
    },
    tags=["schedules"],
    summary="Создать расписание",
    response_model_by_alias=True,
)
async def create_schedule(
    garden_id: UUID = Path(..., description=""),
    schedule_input: ScheduleInput = Body(..., description=""),
) -> Schedule:
    """Зона должна принадлежать саду. Конец интервала строго позже начала."""
    if not BaseSchedulesApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseSchedulesApi.subclasses[0]().create_schedule(garden_id, schedule_input)


@router.delete(
    "/gardens/{garden_id}/schedules/{schedule_id}",
    status_code=204,
    response_model=None,
    responses={
        204: {"description": "Запись удалена"},
        404: {"model": Error, "description": "NOT_FOUND - ресурс не найден."},
        500: {"model": Error, "description": "Внутренняя ошибка сервера."},
    },
    tags=["schedules"],
    summary="Удалить расписание",
    response_model_by_alias=True,
)
async def delete_schedule(
    garden_id: UUID = Path(..., description=""),
    schedule_id: UUID = Path(..., description=""),
) -> None:
    if not BaseSchedulesApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseSchedulesApi.subclasses[0]().delete_schedule(garden_id, schedule_id)
