# src/graph_loader.py

from rdflib import Graph
from SPARQLWrapper import (
    SPARQLWrapper, 
    GET, 
    TURTLE
    )
from pathlib import Path
from typing import Union, Literal


def load_graph(source: dict) -> Graph:
    """
    Load an RDF graph from a file or a SPARQL endpoint.

    This function creates an RDFLib `Graph` instance and populates it with triples 
    either by parsing a local RDF file or by querying a SPARQL endpoint using a 
    `CONSTRUCT` query that retrieves all triples.

    Args:
        source (dict): A dictionary specifying the RDF source. Must contain:
            - **type** (str): The source type, either `"file"` or `"sparql"`.
            - **file_path** (str, optional): Path to the RDF file (required if type is `"file"`).
            - **file_format** (str, optional): RDF serialization format (e.g., `"turtle"`, `"xml"`).
            - **sparql_endpoint** (str, optional): URL of the SPARQL endpoint 
              (required if type is `"sparql"`).

    Returns:
        Graph: An RDFLib `Graph` populated with triples from the specified source.

    Raises:
        ValueError: If the `type` key is not `"file"` or `"sparql"`.
        KeyError: If required keys for the chosen source type are missing.

    Example:
        >>> source_file = {
        ...     "type": "file",
        ...     "file_path": "data.ttl",
        ...     "file_format": "turtle"
        ... }
        >>> g = load_graph(source_file)
        >>> len(g)
        42

        >>> source_sparql = {
        ...     "type": "sparql",
        ...     "sparql_endpoint": "https://example.org/sparql"
        ... }
        >>> g = load_graph(source_sparql)
    """
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
