# src/graph_loader.py
from rdflib import Graph
from SPARQLWrapper import SPARQLWrapper, GET, TURTLE
from pathlib import Path
from typing import Union, Literal


def load_graph(source: dict) -> Graph:
    g = Graph()
    if source["type"] == "file":
        g.parse(str(source["file_path"]), format=source["file_format"])
    elif source["type"] == "sparql":
        endpoint = source["sparql_endpoint"]
        sparql = SPARQLWrapper(endpoint)
        sparql.setQuery("CONSTRUCT { ?s ?p ?o } WHERE { ?s ?p ?o }")
        sparql.setMethod(GET)
        sparql.setReturnFormat(TURTLE)
        result = sparql.query().convert()
        g.parse(data=result, format="turtle")
    else:
        raise ValueError("Unsupported source type. Must be 'file' or 'sparql'.")
    return g
