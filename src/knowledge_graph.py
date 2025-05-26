from rdflib import Graph, URIRef, RDF, Literal, Namespace
from src.utils import get_uri_label, uri_to_filename, get_namespace, generate_path, remove_root
from collections import defaultdict
from SPARQLWrapper import SPARQLWrapper, GET, TURTLE
import pygal, logging, requests


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
            query = """
                CONSTRUCT { ?s ?p ?o }
                WHERE { ?s ?p ?o }
            """
            sparql = SPARQLWrapper(self.source)
            sparql.setQuery(query)
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


        '''
    def generate_bar(self, title, data):
        bar_chart = pygal.HorizontalBar(
            style=pygal.style.Style(
                background="white",
                plot_background="white",
                opacity=".6",
                opacity_hover=".8",
                value_colors=("black",)
            )
        )
        bar_chart.title = title
        for d in data:
            bar_chart.add(d["label"], d["frequency"])
        return bar_chart.render(
            legend_at_bottom=True,
            legend_box_size=5,
            legend_at_bottom_columns=3,
            order_min=1,
            ).decode("utf-8")
        '''
