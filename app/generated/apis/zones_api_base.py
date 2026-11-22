# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from typing import Any, List
from uuid import UUID
from app.generated.models.error import Error
from app.generated.models.zone import Zone
from app.generated.models.zone_input import ZoneInput


class BaseZonesApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseZonesApi.subclasses = BaseZonesApi.subclasses + (cls,)
    async def list_zones(
        self,
        garden_id: UUID,
    ) -> List[Zone]:
        ...


    async def create_zone(
        self,
        garden_id: UUID,
        zone_input: ZoneInput,
    ) -> Zone:
        """Все деревья принадлежат данному саду."""
        ...


    async def get_zone(
        self,
        garden_id: UUID,
        zone_id: UUID,
    ) -> Zone:
        ...


    async def update_zone(
        self,
        garden_id: UUID,
        zone_id: UUID,
        zone_input: ZoneInput,
    ) -> Zone:
        """Все деревья принадлежат данному саду."""
        ...


    async def delete_zone(
        self,
        garden_id: UUID,
        zone_id: UUID,
    ) -> None:
        """Удаляет расписания зоны."""
        ...
