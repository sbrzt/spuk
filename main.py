from src.rdf_graph import RDFGraph
from src.html_page import HTMLPage, IndexPage

def main():
    rdf = RDFGraph("data/data.ttl")
    entities = rdf.get_entities()

    for entity in entities:
        properties = rdf.get_properties(entity)
        page = HTMLPage(entity, properties)
        page.save()

    index_page = IndexPage(entities)
    index_page.save()

    print("🎉 All pages generated successfully!")

if __name__ == "__main__":
    main()
