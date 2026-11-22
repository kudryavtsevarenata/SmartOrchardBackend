# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from app.generated.apis.notes_api_base import BaseNotesApi
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

from typing import List
from uuid import UUID
from app.generated.models.error import Error
from app.generated.models.note_input import NoteInput
from app.generated.models.tree_note import TreeNote

router = APIRouter()

ns_pkg = app.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/gardens/{garden_id}/trees/{tree_id}/notes",
    responses={
        200: {"model": List[TreeNote], "description": "Успешный ответ"},
        404: {"model": Error, "description": "NOT_FOUND - ресурс не найден."},
        500: {"model": Error, "description": "Внутренняя ошибка сервера."},
    },
    tags=["notes"],
    summary="Список заметок дерева",
    response_model_by_alias=True,
)
async def list_notes(
    garden_id: UUID = Path(..., description=""),
    tree_id: UUID = Path(..., description=""),
) -> List[TreeNote]:
    """Сортировка по убыванию created_at."""
    if not BaseNotesApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseNotesApi.subclasses[0]().list_notes(garden_id, tree_id)


@router.post(
    "/gardens/{garden_id}/trees/{tree_id}/notes",
    status_code=201,
    responses={
        201: {"model": TreeNote, "description": "Запись создана"},
        404: {"model": Error, "description": "NOT_FOUND - ресурс не найден."},
        422: {"model": Error, "description": "VALIDATION_ERROR - ошибка валидации."},
        500: {"model": Error, "description": "Внутренняя ошибка сервера."},
    },
    tags=["notes"],
    summary="Создать заметку",
    response_model_by_alias=True,
)
async def create_note(
    garden_id: UUID = Path(..., description=""),
    tree_id: UUID = Path(..., description=""),
    note_input: NoteInput = Body(..., description=""),
) -> TreeNote:
    if not BaseNotesApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseNotesApi.subclasses[0]().create_note(garden_id, tree_id, note_input)
