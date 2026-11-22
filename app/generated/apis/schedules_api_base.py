# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from datetime import date
from pydantic import Field
from typing import Any, List, Optional
from typing_extensions import Annotated
from uuid import UUID
from app.generated.models.error import Error
from app.generated.models.schedule import Schedule
from app.generated.models.schedule_input import ScheduleInput


class BaseSchedulesApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseSchedulesApi.subclasses = BaseSchedulesApi.subclasses + (cls,)
    async def list_schedules(
        self,
        garden_id: UUID,
        zone_id: Annotated[Optional[UUID], Field(description="Зона полива")],
        var_date: Annotated[Optional[date], Field(description="Интервалы, пересекающие этот день")],
    ) -> List[Schedule]:
        """Сортировка по start."""
        ...


    async def create_schedule(
        self,
        garden_id: UUID,
        schedule_input: ScheduleInput,
    ) -> Schedule:
        """Зона должна принадлежать саду. Конец интервала строго позже начала."""
        ...


    async def delete_schedule(
        self,
        garden_id: UUID,
        schedule_id: UUID,
    ) -> None:
        ...
