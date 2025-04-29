from pydantic import BaseModel

class SPARQLQuery(BaseModel):
    query: str