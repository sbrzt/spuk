from jinja2 import Environment, FileSystemLoader
from src.utils import escape_html, uri_to_filename, get_uri_label
import os

env = Environment(loader=FileSystemLoader("static/templates"))

class HTMLPage:
    def __init__(self, subject, properties):
        """Initializes the HTMLPage with subject and its properties."""
        self.subject = subject
        self.properties = properties

    def render(self):
        """Generates the HTML for the entity subject."""
        template = env.get_template("entity.html")
        return template.render(
            subject_uri = self.subject, 
            subject_label = self.subject,
            properties = self.properties
        )

    def save(self, output_dir="docs"):
        """Saves the HTML page to the output directory."""
        html = self.render()
        filename = uri_to_filename(self.subject)
        output_path = f"{output_dir}/{filename}"
        os.makedirs(output_dir, exist_ok=True)
        with open(output_path, "w") as f:
            f.write(html)
        print(f"✅ Saved HTML for {self.subject} to {output_path}")


class IndexPage:
    def __init__(self, entities, summary):
        """Initializes the IndexPage with the list of entities."""
        self.entities = entities
        self.summary = summary

    def render(self):
        """Generates the HTML for the index page."""
        template = env.get_template("index.html")
        items = [
            {
                "label": str(entity),
                "filename": uri_to_filename(str(entity))
            }
            for entity in self.entities
        ]
        return template.render(entities=items, summary=self.summary)

    def save(self, output_dir="docs"):
        """Saves the index HTML page."""
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, "index.html"), "w") as f:
            f.write(self.render())
        print(f"✅ Saved index page to {output_dir}/index.html")