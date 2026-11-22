# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from app.generated.apis.trees_api_base import BaseTreesApi
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

from pydantic import Field
from typing import List, Optional
from typing_extensions import Annotated
from uuid import UUID
from app.generated.models.error import Error
from app.generated.models.tree import Tree
from app.generated.models.tree_lookup import TreeLookup
from app.generated.models.tree_status import TreeStatus

router = APIRouter()

ns_pkg = app.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/gardens/{garden_id}/trees",
    responses={
        200: {"model": List[Tree], "description": "Успешный ответ"},
        404: {"model": Error, "description": "NOT_FOUND - ресурс не найден."},
        500: {"model": Error, "description": "Внутренняя ошибка сервера."},
    },
    tags=["trees"],
    summary="Список деревьев сада",
    response_model_by_alias=True,
)
async def list_trees(
    garden_id: UUID = Path(..., description=""),
    row: Annotated[Optional[Annotated[int, Field(ge=1)]], Field(description="Номер ряда")] = Query(None, description="Номер ряда", alias="row", ge=1),
    status: Annotated[Optional[TreeStatus], Field(description="Состояние")] = Query(None, description="Состояние", alias="status"),
) -> List[Tree]:
    if not BaseTreesApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseTreesApi.subclasses[0]().list_trees(garden_id, row, status)


@router.get(
    "/gardens/{garden_id}/trees/lookup",
    responses={
        200: {"model": Tree, "description": "Успешный ответ"},
        404: {"model": Error, "description": "NOT_FOUND - ресурс не найден."},
        500: {"model": Error, "description": "Внутренняя ошибка сервера."},
    },
    tags=["trees"],
    summary="Поиск дерева по ряду и месту",
    response_model_by_alias=True,
)
async def lookup_tree(
    row: Annotated[int, Field(ge=1, description="Номер ряда")] = Query(..., description="Номер ряда", alias="row", ge=1),
    place: Annotated[int, Field(ge=1, description="Место в ряду")] = Query(..., description="Место в ряду", alias="place", ge=1),
    garden_id: UUID = Path(..., description=""),
) -> Tree:
    if not BaseTreesApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseTreesApi.subclasses[0]().lookup_tree(row, place, garden_id)


@router.get(
    "/gardens/{garden_id}/trees/{tree_id}",
    responses={
        200: {"model": Tree, "description": "Успешный ответ"},
        404: {"model": Error, "description": "NOT_FOUND - ресурс не найден."},
        500: {"model": Error, "description": "Внутренняя ошибка сервера."},
    },
    tags=["trees"],
    summary="Получить дерево",
    response_model_by_alias=True,
)
async def get_tree(
    garden_id: UUID = Path(..., description=""),
    tree_id: UUID = Path(..., description=""),
) -> Tree:
    if not BaseTreesApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseTreesApi.subclasses[0]().get_tree(garden_id, tree_id)


@router.get(
    "/trees/lookup-qr",
    responses={
        200: {"model": TreeLookup, "description": "Успешный ответ"},
        400: {"model": Error, "description": "INVALID_QR"},
        404: {"model": Error, "description": "NOT_FOUND"},
        500: {"model": Error, "description": "Внутренняя ошибка сервера."},
    },
    tags=["trees"],
    summary="Поиск дерева по QR-коду",
    response_model_by_alias=True,
)
async def lookup_qr(
    code: Annotated[str, Field(description="Содержимое QR-метки smartorchard://tree/<uuid>")] = Query(..., description="Содержимое QR-метки smartorchard://tree/&lt;uuid&gt;", alias="code"),
) -> TreeLookup:
    if not BaseTreesApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseTreesApi.subclasses[0]().lookup_qr(code)
