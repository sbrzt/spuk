import tomllib
from rdflib import Graph
from SPARQLWrapper import SPARQLWrapper, GET, TURTLE

with open("config.toml", "rb") as f:
    configuration = tomllib.load(f)

QUERY = configuration["knowledge_graph"]["query"]


class KnowledgeGraph:
    """
    A wrapper around rdflib.Graph for data source abstraction.
    It handles loading RDF data from either a file or a SPARQL 
    endpoint, and stores basic metadata.
    """
    def __init__(
        self, 
        source: str, 
        is_sparql_endpoint: bool = False
        ) -> None:

        self.source: str = source
        self._is_sparql_endpoint: bool = is_sparql_endpoint
        self._graph: Graph = self.load()
        
    
    def load(
        self,
        ) -> Graph:

        g = Graph()
        if self._is_sparql_endpoint:
            sparql = SPARQLWrapper(self.source)
            sparql.setQuery(QUERY)
            sparql.setMethod(GET)
            sparql.setReturnFormat(TURTLE)
            response = sparql.query().convert()
            g.parse(
                data = response.decode("utf-8"), 
                format = "turtle"
            )
        else:
            g.parse(self.source)
        print(f"✅ Data loaded from {self.source}.")
        return g


    def get_graph(
        self
        ) -> Graph:

        return self._graph
