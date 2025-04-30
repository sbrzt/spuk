from pydantic import BaseModel, Field

class SPARQLQuery(BaseModel):
    query: str = Field(
        ...,
        example="SELECT ?s ?p ?o WHERE {?s ?p ?o .} LIMIT 10"
        )