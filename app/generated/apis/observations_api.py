# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from app.generated.apis.observations_api_base import BaseObservationsApi
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

from pydantic import Field, StrictBool, StrictBytes, StrictStr
from typing import List, Optional, Tuple, Union
from typing_extensions import Annotated
from uuid import UUID
from app.generated.models.ai_result import AiResult
from app.generated.models.error import Error
from app.generated.models.observation import Observation
from app.generated.models.tree_status import TreeStatus
from fastapi import File, UploadFile

router = APIRouter()

ns_pkg = app.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/gardens/{garden_id}/trees/{tree_id}/observations",
    responses={
        200: {"model": List[Observation], "description": "Успешный ответ"},
        404: {"model": Error, "description": "NOT_FOUND - ресурс не найден."},
        500: {"model": Error, "description": "Внутренняя ошибка сервера."},
    },
    tags=["observations"],
    summary="Список осмотров дерева",
    response_model_by_alias=True,
)
async def list_observations(
    garden_id: UUID = Path(..., description=""),
    tree_id: UUID = Path(..., description=""),
) -> List[Observation]:
    """Сортировка по убыванию created_at."""
    if not BaseObservationsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseObservationsApi.subclasses[0]().list_observations(garden_id, tree_id)


@router.post(
    "/gardens/{garden_id}/trees/{tree_id}/observations",
    status_code=201,
    responses={
        201: {"model": Observation, "description": "Запись создана"},
        404: {"model": Error, "description": "NOT_FOUND - ресурс не найден."},
        422: {"model": Error, "description": "VALIDATION_ERROR - ошибка валидации."},
        500: {"model": Error, "description": "Внутренняя ошибка сервера."},
    },
    tags=["observations"],
    summary="Создать осмотр",
    response_model_by_alias=True,
)
async def create_observation(
    garden_id: UUID = Path(..., description=""),
    tree_id: UUID = Path(..., description=""),
    status: TreeStatus = Form(..., description="", alias="status"),
    comment: Optional[StrictStr] = Form(None, description="", alias="comment"),
    diagnosis: Optional[StrictStr] = Form(None, description="", alias="diagnosis"),
    recommendations: Optional[StrictStr] = Form(None, description="", alias="recommendations"),
    sample_photo: Optional[StrictBool] = Form(None, description="", alias="sample_photo"),
    photo: Optional[UploadFile] = File(None, description="JPEG или PNG, до 10 МБ.", alias="photo"),
    original_ai: Optional[AiResult] = Form(None, description="", alias="original_ai"),
) -> Observation:
    """Обновляет состояние дерева. Для ручного осмотра нужны комментарий, фото или изменение статуса. При использовании ИИ заполните диагноз и рекомендации. Исходный ответ модели можно сохранить в original_ai."""
    if not BaseObservationsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseObservationsApi.subclasses[0]().create_observation(garden_id, tree_id, status, comment, diagnosis, recommendations, sample_photo, photo, original_ai)


@router.get(
    "/gardens/{garden_id}/trees/{tree_id}/observations/{observation_id}",
    responses={
        200: {"model": Observation, "description": "Успешный ответ"},
        404: {"model": Error, "description": "NOT_FOUND - ресурс не найден."},
        500: {"model": Error, "description": "Внутренняя ошибка сервера."},
    },
    tags=["observations"],
    summary="Получить осмотр",
    response_model_by_alias=True,
)
async def get_observation(
    garden_id: UUID = Path(..., description=""),
    tree_id: UUID = Path(..., description=""),
    observation_id: UUID = Path(..., description=""),
) -> Observation:
    if not BaseObservationsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseObservationsApi.subclasses[0]().get_observation(garden_id, tree_id, observation_id)
