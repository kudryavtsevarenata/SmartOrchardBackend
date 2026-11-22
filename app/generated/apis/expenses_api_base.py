# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from datetime import date
from pydantic import Field
from typing import List, Optional
from typing_extensions import Annotated
from uuid import UUID
from app.generated.models.error import Error
from app.generated.models.expense import Expense
from app.generated.models.expense_input import ExpenseInput


class BaseExpensesApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseExpensesApi.subclasses = BaseExpensesApi.subclasses + (cls,)
    async def list_expenses(
        self,
        garden_id: UUID,
        category: Annotated[Optional[str], Field(description="Категория")],
        var_from: Annotated[Optional[date], Field(description="Начало диапазона включительно")],
        to: Annotated[Optional[date], Field(description="Конец диапазона включительно")],
    ) -> List[Expense]:
        ...


    async def create_expense(
        self,
        garden_id: UUID,
        expense_input: ExpenseInput,
    ) -> Expense:
        """Категория задаётся свободным текстом. Сервер вычисляет total_cents &#x3D; round(quantity × price × 100)."""
        ...
