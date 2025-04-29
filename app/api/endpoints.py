from fastapi import APIRouter, HTTPException
from app.rdf_graph import RDFGraph
from app.utils import uri_to_filename

router = APIRouter()
rdf = RDFGraph("data/data.ttl")

@router.get("/individuals")
def list_individuals():
    individuals = rdf.get_individuals()
    return {"individuals": [str(i) for i in individuals]}

@router.get("/individuals/{id}")
def get_individual(id: str):
    subject_uri = None
    for s in rdf.get_individuals():
        if uri_to_filename(str(s)) == id + ".html":
            subject_uri = s
            break
    if not subject_uri:
        raise HTTPException(status_code=404, detail="Individual not found")
    props = rdf.get_properties(subject_uri)
    return {
        "subject": str(subject_uri),
        "properties": [{"predicate": str(p), "object": str(o)} for p, o in props]
    }
