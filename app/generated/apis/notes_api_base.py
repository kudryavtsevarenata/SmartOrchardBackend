# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from typing import List
from uuid import UUID
from app.generated.models.error import Error
from app.generated.models.note_input import NoteInput
from app.generated.models.tree_note import TreeNote


class BaseNotesApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseNotesApi.subclasses = BaseNotesApi.subclasses + (cls,)
    async def list_notes(
        self,
        garden_id: UUID,
        tree_id: UUID,
    ) -> List[TreeNote]:
        """Сортировка по убыванию created_at."""
        ...


    async def create_note(
        self,
        garden_id: UUID,
        tree_id: UUID,
        note_input: NoteInput,
    ) -> TreeNote:
        ...
