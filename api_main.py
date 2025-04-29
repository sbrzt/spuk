from fastapi import FastAPI
from app.api.endpoints import router as entities_router
from app.api.sparql import router as sparql_router

app = FastAPI(title="RDF Graph API")

app.include_router(entities_router)
app.include_router(sparql_router)
