# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field
from typing import List, Optional
from typing_extensions import Annotated
from uuid import UUID
from app.generated.models.error import Error
from app.generated.models.tree import Tree
from app.generated.models.tree_lookup import TreeLookup
from app.generated.models.tree_status import TreeStatus


class BaseTreesApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseTreesApi.subclasses = BaseTreesApi.subclasses + (cls,)
    async def list_trees(
        self,
        garden_id: UUID,
        row: Annotated[Optional[Annotated[int, Field(ge=1)]], Field(description="Номер ряда")],
        status: Annotated[Optional[TreeStatus], Field(description="Состояние")],
    ) -> List[Tree]:
        ...


    async def get_tree(
        self,
        garden_id: UUID,
        tree_id: UUID,
    ) -> Tree:
        ...


    async def lookup_tree(
        self,
        row: Annotated[int, Field(ge=1, description="Номер ряда")],
        place: Annotated[int, Field(ge=1, description="Место в ряду")],
        garden_id: UUID,
    ) -> Tree:
        ...


    async def lookup_qr(
        self,
        code: Annotated[str, Field(description="Содержимое QR-метки smartorchard://tree/<uuid>")],
    ) -> TreeLookup:
        ...
