from src.knowledge_graph import KnowledgeGraph
from src.entity_object import EntityObject
from src.index_object import IndexObject
from src.documentation_object import DocumentationObject

def main():
    source = "https://chad-kg.duckdns.org/chadkg/sparql"
    rdf = KnowledgeGraph(source, is_sparql_endpoint=True)
    entities = rdf.get_property_object_data()
    summary = rdf.get_summary()

    pages = []
    for entity, property_object_pairs in entities.items():
        page = EntityObject(
            entity, 
            property_object_pairs,
            rdf
        )
        page.generate_folders()
        page.serialize()
        page.save()
        pages.append(page)

    index_page = IndexObject(pages, summary)
    index_page.save()

    sparql_page = DocumentationObject(source, "sparql")
    sparql_page.save()

    documentation_page = DocumentationObject(source, "documentation")
    documentation_page.save()

    print("🎉 All pages generated successfully!")

if __name__ == "__main__":
    main()
