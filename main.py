from src.knowledge_graph import KnowledgeGraph
from src.profile import Profile
from src.visualizer import Visualizer
from src.entity_object import EntityObject
from src.index_object import IndexObject
from src.documentation_object import DocumentationObject

def main():
    source = "https://chad-kg.duckdns.org/chadkg/sparql"
    kg = KnowledgeGraph(
        source = source, 
        is_sparql_endpoint = True
    )
    profile = Profile(
        knowledge_graph = kg
    )
    visualizer = Visualizer(
        profile = profile
    )

    entities = profile.entities

    pages = []
    for data in entities.values():
        page = EntityObject(
            entity_data = data
        )
        page.generate_folders()
        page.serialize()
        page.save()
        pages.append(page)

    index_page = IndexObject(
        entity_objects = pages,
        profile = profile,
        visualizer = visualizer
        )
    index_page.save()

    sparql_page = DocumentationObject(source, "sparql")
    sparql_page.save()

    documentation_page = DocumentationObject(source, "documentation")
    documentation_page.save()

    print("🎉 All pages generated successfully!")

if __name__ == "__main__":
    main()
