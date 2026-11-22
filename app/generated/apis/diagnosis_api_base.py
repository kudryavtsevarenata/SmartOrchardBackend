# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from typing import Any, Optional
from app.generated.models.ai_result import AiResult
from app.generated.models.error import Error


class BaseDiagnosisApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseDiagnosisApi.subclasses = BaseDiagnosisApi.subclasses + (cls,)
    async def analyze_photo(
        self,
        sample_photo: Optional[Any],
    ) -> AiResult:
        """Запланированный метод для подключения модели. Анализ предшествует сохранению осмотра. Таймаут модели 30 секунд."""
        ...
