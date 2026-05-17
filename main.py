from fastapi import FastAPI

from dashboard import router as dashboard_router
from vapi_webhook import router as vapi_router


app = FastAPI(title="Agent Vocal RDV")
app.include_router(dashboard_router)
app.include_router(vapi_router)


@app.get("/")
def health_check() -> dict[str, str]:
    return {"status": "Agent Vocal RDV actif"}
