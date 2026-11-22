from fastapi import FastAPI

from app.generated.apis.crops_api import router as CropsApiRouter
from app.generated.apis.diagnosis_api import router as DiagnosisApiRouter
from app.generated.apis.expenses_api import router as ExpensesApiRouter
from app.generated.apis.gardens_api import router as GardensApiRouter
from app.generated.apis.notes_api import router as NotesApiRouter
from app.generated.apis.observations_api import router as ObservationsApiRouter
from app.generated.apis.schedules_api import router as SchedulesApiRouter
from app.generated.apis.settings_api import router as SettingsApiRouter
from app.generated.apis.trees_api import router as TreesApiRouter
from app.generated.apis.zones_api import router as ZonesApiRouter

app = FastAPI(
    title="SmartOrchard Backend API",
    version="1.0.0",
)

app.include_router(CropsApiRouter, prefix="/v1")
app.include_router(DiagnosisApiRouter, prefix="/v1")
app.include_router(ExpensesApiRouter, prefix="/v1")
app.include_router(GardensApiRouter, prefix="/v1")
app.include_router(NotesApiRouter, prefix="/v1")
app.include_router(ObservationsApiRouter, prefix="/v1")
app.include_router(SchedulesApiRouter, prefix="/v1")
app.include_router(SettingsApiRouter, prefix="/v1")
app.include_router(TreesApiRouter, prefix="/v1")
app.include_router(ZonesApiRouter, prefix="/v1")
