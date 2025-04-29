from src.rdf_graph import RDFGraph
from src.html_page import HTMLPage, IndexPage

def main():
    rdf = RDFGraph("data/data.ttl")
    individuals = rdf.get_individuals()

    for individual in individuals:
        properties = rdf.get_properties(individual)
        page = HTMLPage(individual, properties)
        page.save()

    index_page = IndexPage(individuals)
    index_page.save()

    print("🎉 All pages generated successfully!")

if __name__ == "__main__":
    main()
