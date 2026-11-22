# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from typing import Any, List
from uuid import UUID
from app.generated.models.error import Error
from app.generated.models.finance import Finance
from app.generated.models.garden import Garden
from app.generated.models.garden_input import GardenInput


class BaseGardensApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseGardensApi.subclasses = BaseGardensApi.subclasses + (cls,)
    async def list_gardens(
        self,
    ) -> List[Garden]:
        ...


    async def create_garden(
        self,
        garden_input: GardenInput,
    ) -> Garden:
        """Культура должна существовать. Число деревьев &#x3D; floor(area_ha × 10000 / (row_spacing × tree_spacing)), от 1 до 10000. Ряды и места нумеруются с 1. Максимум 100 рядов. Начальный статус UNKNOWN."""
        ...


    async def get_garden(
        self,
        garden_id: UUID,
    ) -> Garden:
        ...


    async def delete_garden(
        self,
        garden_id: UUID,
    ) -> None:
        """Удаляет также деревья, зоны, расписания, затраты, осмотры и заметки сада."""
        ...


    async def update_finance(
        self,
        garden_id: UUID,
        finance: Finance,
    ) -> Finance:
        ...
