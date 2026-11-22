import os

import psycopg
from psycopg.rows import class_row
from starlette.concurrency import run_in_threadpool

from app.generated.apis.crops_api_base import BaseCropsApi
from app.generated.models.crop import Crop


def read_crops() -> list[Crop]:
    with psycopg.connect(os.environ["DATABASE_URL"], row_factory=class_row(Crop)) as conn:
        return conn.execute("""
            SELECT id, name, variety, row_spacing::text, tree_spacing::text, prefix
            FROM crops ORDER BY name
        """).fetchall()


class CropsApi(BaseCropsApi):
    async def list_crops(self) -> list[Crop]:
        return await run_in_threadpool(read_crops)
