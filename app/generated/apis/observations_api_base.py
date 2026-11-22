# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field, StrictBool, StrictBytes, StrictStr
from typing import List, Optional, Tuple, Union
from typing_extensions import Annotated
from uuid import UUID
from app.generated.models.ai_result import AiResult
from app.generated.models.error import Error
from app.generated.models.observation import Observation
from app.generated.models.tree_status import TreeStatus
from fastapi import File, UploadFile


class BaseObservationsApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseObservationsApi.subclasses = BaseObservationsApi.subclasses + (cls,)
    async def list_observations(
        self,
        garden_id: UUID,
        tree_id: UUID,
    ) -> List[Observation]:
        """Сортировка по убыванию created_at."""
        ...


    async def create_observation(
        self,
        garden_id: UUID,
        tree_id: UUID,
        status: TreeStatus,
        comment: Optional[StrictStr],
        diagnosis: Optional[StrictStr],
        recommendations: Optional[StrictStr],
        sample_photo: Optional[StrictBool],
        photo: Optional[UploadFile],
        original_ai: Optional[AiResult],
    ) -> Observation:
        """Обновляет состояние дерева. Для ручного осмотра нужны комментарий, фото или изменение статуса. При использовании ИИ заполните диагноз и рекомендации. Исходный ответ модели можно сохранить в original_ai."""
        ...


    async def get_observation(
        self,
        garden_id: UUID,
        tree_id: UUID,
        observation_id: UUID,
    ) -> Observation:
        ...
