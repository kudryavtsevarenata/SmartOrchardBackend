# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from app.generated.apis.crops_api_base import BaseCropsApi
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
from app.generated.models.crop import Crop
from app.generated.models.crop_input import CropInput
from app.generated.models.error import Error

router = APIRouter()

ns_pkg = app.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/crops",
    responses={
        200: {"model": List[Crop], "description": "Успешный ответ"},
        500: {"model": Error, "description": "Внутренняя ошибка сервера."},
    },
    tags=["crops"],
    summary="Список культур",
    response_model_by_alias=True,
)
async def list_crops(
) -> List[Crop]:
    if not BaseCropsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseCropsApi.subclasses[0]().list_crops()


@router.post(
    "/crops",
    status_code=201,
    responses={
        201: {"model": Crop, "description": "Запись создана"},
        409: {"model": Error, "description": "DUPLICATE - совпадают название, сорт и оба посадочных расстояния."},
        422: {"model": Error, "description": "VALIDATION_ERROR - ошибка валидации."},
        500: {"model": Error, "description": "Внутренняя ошибка сервера."},
    },
    tags=["crops"],
    summary="Создать культуру",
    response_model_by_alias=True,
)
async def create_crop(
    crop_input: CropInput = Body(..., description=""),
) -> Crop:
    """При отсутствии prefix сервер формирует его из названия."""
    if not BaseCropsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseCropsApi.subclasses[0]().create_crop(crop_input)


@router.get(
    "/crops/{crop_id}",
    responses={
        200: {"model": Crop, "description": "Успешный ответ"},
        404: {"model": Error, "description": "NOT_FOUND - ресурс не найден."},
        500: {"model": Error, "description": "Внутренняя ошибка сервера."},
    },
    tags=["crops"],
    summary="Получить культуру",
    response_model_by_alias=True,
)
async def get_crop(
    crop_id: UUID = Path(..., description=""),
) -> Crop:
    if not BaseCropsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseCropsApi.subclasses[0]().get_crop(crop_id)


@router.put(
    "/crops/{crop_id}",
    responses={
        200: {"model": Crop, "description": "Успешный ответ"},
        404: {"model": Error, "description": "NOT_FOUND - ресурс не найден."},
        409: {"model": Error, "description": "DUPLICATE - совпадают название, сорт и оба посадочных расстояния."},
        422: {"model": Error, "description": "VALIDATION_ERROR - ошибка валидации."},
        500: {"model": Error, "description": "Внутренняя ошибка сервера."},
    },
    tags=["crops"],
    summary="Обновить культуру",
    response_model_by_alias=True,
)
async def update_crop(
    crop_id: UUID = Path(..., description=""),
    crop_input: CropInput = Body(..., description=""),
) -> Crop:
    if not BaseCropsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseCropsApi.subclasses[0]().update_crop(crop_id, crop_input)


@router.delete(
    "/crops/{crop_id}",
    status_code=204,
    response_model=None,
    responses={
        204: {"description": "Запись удалена"},
        404: {"model": Error, "description": "NOT_FOUND - ресурс не найден."},
        409: {"model": Error, "description": "CONFLICT - культура используется в саду."},
        500: {"model": Error, "description": "Внутренняя ошибка сервера."},
    },
    tags=["crops"],
    summary="Удалить культуру",
    response_model_by_alias=True,
)
async def delete_crop(
    crop_id: UUID = Path(..., description=""),
) -> None:
    if not BaseCropsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseCropsApi.subclasses[0]().delete_crop(crop_id)
