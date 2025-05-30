from jinja2 import Environment, FileSystemLoader
from rdflib import Graph, URIRef, Literal, RDF
from urllib.parse import urlparse
from typing import List
from src.entity_object import EntityObject
from src.profile import Profile
from src.visualizer import Visualizer
import os

env = Environment(loader=FileSystemLoader("static/templates"))

class IndexObject:
    def __init__(
        self, 
        entity_objects: List[EntityObject],
        profile: Profile,
        visualizer: Visualizer
        ):
        self.source = profile.source
        self.entities = entity_objects
        self.summary = profile.get_summary()
        self.chart_properties = visualizer.most_frequent_properties_chart()
        self.chart_classes = visualizer.most_frequent_classes_chart()
        self.chart_models = visualizer.most_frequent_models_chart()
        self.chart_entities = visualizer.most_frequent_entities_chart()

    def render(
        self
        ) -> None:
        template = env.get_template("index.html")
        return template.render(
            source = self.source,
            entities = self.entities, 
            summary = self.summary,
            chart_classes = self.chart_classes,
            chart_properties = self.chart_properties,
            chart_models = self.chart_models,
            chart_entities = self.chart_entities
        )

    def save(
        self, 
        output_dir = "docs"
        ) -> None:
        os.makedirs(
            output_dir, 
            exist_ok = True
            )
        with open(os.path.join(output_dir, "index.html"), "w") as f:
            f.write(self.render())
        print(f"✅ Saved index page to {output_dir}/index.html")