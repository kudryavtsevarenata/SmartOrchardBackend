# coding: utf-8

from fastapi import HTTPException

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from typing import Any, List
from uuid import UUID
from app.generated.models.crop import Crop
from app.generated.models.crop_input import CropInput
from app.generated.models.error import Error


class BaseCropsApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseCropsApi.subclasses = BaseCropsApi.subclasses + (cls,)
    async def list_crops(
        self,
    ) -> List[Crop]:
        raise HTTPException(status_code=500, detail="Not implemented")


    async def create_crop(
        self,
        crop_input: CropInput,
    ) -> Crop:
        """При отсутствии prefix сервер формирует его из названия."""
        raise HTTPException(status_code=500, detail="Not implemented")


    async def get_crop(
        self,
        crop_id: UUID,
    ) -> Crop:
        raise HTTPException(status_code=500, detail="Not implemented")


    async def update_crop(
        self,
        crop_id: UUID,
        crop_input: CropInput,
    ) -> Crop:
        raise HTTPException(status_code=500, detail="Not implemented")


    async def delete_crop(
        self,
        crop_id: UUID,
    ) -> None:
        raise HTTPException(status_code=500, detail="Not implemented")
