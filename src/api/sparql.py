from fastapi import APIRouter, HTTPException
from rdflib.plugins.sparql.processor import SPARQLResult
from src.api.schema import SPARQLQuery
from src.rdf_graph import RDFGraph

router = APIRouter()
rdf = RDFGraph("data/data.ttl")

@router.post("/sparql")
def sparql_query(query: SPARQLQuery):
    try:
        result: SPARQLResult = rdf.graph.query(query.query)

        if result.type == 'SELECT':
            vars = result.vars
            bindings = []
            for row in result:
                bindings.append({str(var): str(row[var]) for var in vars})
            return {"results": bindings}

        elif result.type == 'ASK':
            return {"result": bool(result)}

        else:
            return {"message": "Only SELECT and ASK queries are supported."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
