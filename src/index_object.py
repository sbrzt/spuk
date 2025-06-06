from jinja2 import Environment, FileSystemLoader
from rdflib import Graph, URIRef, Literal, RDF
from urllib.parse import urlparse
from typing import List
from src.entity_object import EntityObject
from src.profile import Profile
from src.visualizer import Visualizer
import os, tomllib

env = Environment(loader=FileSystemLoader("static/templates"))
with open("config.toml", "rb") as f:
    configuration = tomllib.load(f)

ROOT_DIR = configuration["general"]["root_dir"]

class IndexObject:
    def __init__(
        self, 
        entity_objects: List[EntityObject],
        profile: Profile,
        visualizer: Visualizer
        ):
        self.source = profile.source
        self.entities = entity_objects
        self.num_entities = profile.num_entities
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
            num_entities = self.num_entities,
            summary = self.summary,
            chart_classes = self.chart_classes,
            chart_properties = self.chart_properties,
            chart_models = self.chart_models,
            chart_entities = self.chart_entities
        )

    def save(
        self
        ) -> None:
        os.makedirs(
            ROOT_DIR, 
            exist_ok = True
            )
        with open(os.path.join(ROOT_DIR, "index.html"), "w") as f:
            f.write(self.render())
        print(f"✅ Saved index page to {ROOT_DIR}/index.html")