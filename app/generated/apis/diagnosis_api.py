# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from app.generated.apis.diagnosis_api_base import BaseDiagnosisApi
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

from typing import Any, Optional
from app.generated.models.ai_result import AiResult
from app.generated.models.error import Error

router = APIRouter()

ns_pkg = app.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/diagnosis/analyze",
    responses={
        200: {"model": AiResult, "description": "Успешный ответ"},
        400: {"model": Error, "description": "NO_PHOTO"},
        422: {"model": Error, "description": "ANALYSIS_FAILED"},
        429: {"model": Error, "description": "Превышен лимит запросов."},
        500: {"model": Error, "description": "Внутренняя ошибка сервера."},
        503: {"model": Error, "description": "SERVICE_UNAVAILABLE"},
    },
    tags=["diagnosis"],
    summary="Запустить анализ",
    response_model_by_alias=True,
)
async def analyze_photo(
    sample_photo: Optional[Any] = Form(..., description="", alias="sample_photo"),
) -> AiResult:
    """Запланированный метод для подключения модели. Анализ предшествует сохранению осмотра. Таймаут модели 30 секунд."""
    if not BaseDiagnosisApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDiagnosisApi.subclasses[0]().analyze_photo(sample_photo)
