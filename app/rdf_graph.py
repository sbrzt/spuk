from rdflib import Graph

class RDFGraph:
    def __init__(self, rdf_file: str):
        self.graph = Graph()
        self.graph.parse(rdf_file)
        print(f"🔗 Loaded {len(self.graph)} triples from {rdf_file}")

    def get_individuals(self):
        """Return all unique subjects in the RDF graph."""
        return list(set(self.graph.subjects()))

    def get_properties(self, subject):
        """Return all (predicate, object) pairs for a given subject."""
        return list(self.graph.predicate_objects(subject))
