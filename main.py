from src.rdf_graph import RDFGraph
from src.html_page import HTMLPage, IndexPage

def main():
    rdf = RDFGraph("https://ddceramics.duckdns.org/ceramics/sparql", is_sparql_endpoint=True)
    entities = rdf.get_property_object_data()
    summary = rdf.get_summary()

    for entity, property_object_pairs in entities.items():
        page = HTMLPage(entity, property_object_pairs)
        page.save()

    index_page = IndexPage(entities.keys(), summary)
    index_page.save()

    print("🎉 All pages generated successfully!")

if __name__ == "__main__":
    main()
