# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from app.generated.apis.expenses_api_base import BaseExpensesApi
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
from typing import List, Optional
from typing_extensions import Annotated
from uuid import UUID
from app.generated.models.error import Error
from app.generated.models.expense import Expense
from app.generated.models.expense_input import ExpenseInput

router = APIRouter()

ns_pkg = app.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/gardens/{garden_id}/expenses",
    responses={
        200: {"model": List[Expense], "description": "Успешный ответ"},
        404: {"model": Error, "description": "NOT_FOUND - ресурс не найден."},
        500: {"model": Error, "description": "Внутренняя ошибка сервера."},
    },
    tags=["expenses"],
    summary="Список затрат сада",
    response_model_by_alias=True,
)
async def list_expenses(
    garden_id: UUID = Path(..., description=""),
    category: Annotated[Optional[str], Field(description="Категория")] = Query(None, description="Категория", alias="category"),
    var_from: Annotated[Optional[date], Field(description="Начало диапазона включительно")] = Query(None, description="Начало диапазона включительно", alias="from"),
    to: Annotated[Optional[date], Field(description="Конец диапазона включительно")] = Query(None, description="Конец диапазона включительно", alias="to"),
) -> List[Expense]:
    if not BaseExpensesApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseExpensesApi.subclasses[0]().list_expenses(garden_id, category, var_from, to)


@router.post(
    "/gardens/{garden_id}/expenses",
    status_code=201,
    responses={
        201: {"model": Expense, "description": "Запись создана"},
        404: {"model": Error, "description": "NOT_FOUND - ресурс не найден."},
        422: {"model": Error, "description": "VALIDATION_ERROR - ошибка валидации."},
        500: {"model": Error, "description": "Внутренняя ошибка сервера."},
    },
    tags=["expenses"],
    summary="Создать затрату",
    response_model_by_alias=True,
)
async def create_expense(
    garden_id: UUID = Path(..., description=""),
    expense_input: ExpenseInput = Body(..., description=""),
) -> Expense:
    """Категория задаётся свободным текстом. Сервер вычисляет total_cents &#x3D; round(quantity × price × 100)."""
    if not BaseExpensesApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseExpensesApi.subclasses[0]().create_expense(garden_id, expense_input)
