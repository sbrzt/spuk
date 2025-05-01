from fastapi import FastAPI
from src.api.endpoints import router as entities_router
from src.api.sparql import router as sparql_router

app = FastAPI(title="SPUK API")

app.include_router(entities_router)
app.include_router(sparql_router)
