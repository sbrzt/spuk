from fastapi import APIRouter, HTTPException
from src.rdf_graph import RDFGraph
from src.utils import uri_to_filename

router = APIRouter()
rdf = RDFGraph("data/data.ttl")

@router.get("/entities")
def list_entities():
    entities = rdf.get_entities()
    return {"entities": [str(i) for i in entities]}

@router.get("/entities/{id}")
def get_entity(id: str):
    subject_uri = None
    for s in rdf.get_entities():
        if uri_to_filename(str(s)) == id + ".html":
            subject_uri = s
            break
    if not subject_uri:
        raise HTTPException(status_code=404, detail="entity not found")
    props = rdf.get_properties(subject_uri)
    return {
        "subject": str(subject_uri),
        "properties": [{"predicate": str(p), "object": str(o)} for p, o in props]
    }
