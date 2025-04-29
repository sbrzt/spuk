from app.utils import escape_html, uri_to_filename
import os

class HTMLPage:
    def __init__(self, subject, properties):
        """Initializes the HTMLPage with subject and its properties."""
        self.subject = subject
        self.properties = properties

    def render(self):
        """Generates the HTML for the individual subject."""
        # Start HTML structure
        html = [f"<html><head><title>{escape_html(str(self.subject))}</title></head><body>"]
        
        # Heading with subject URI
        html.append(f"<h1>{escape_html(str(self.subject))}</h1>")
        
        # Property list
        html.append("<ul>")
        for predicate, obj in self.properties:
            html.append(f"<li><strong>{escape_html(str(predicate))}:</strong> {escape_html(str(obj))}</li>")
        html.append("</ul>")
        
        # Back link to index
        html.append('<p><a href="index.html">Back to index</a></p>')

        # Close the HTML tags
        html.append("</body></html>")
        
        return "\n".join(html)

    def save(self, output_dir="docs"):
        """Saves the HTML page to the output directory."""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        filename = uri_to_filename(str(self.subject))
        with open(f"{output_dir}/{filename}", "w") as f:
            f.write(self.render())
        print(f"✅ Saved HTML for {self.subject} to {output_dir}/{filename}")


class IndexPage:
    def __init__(self, individuals):
        """Initializes the IndexPage with the list of individuals."""
        self.individuals = individuals

    def render(self):
        """Generates the HTML for the index page."""
        html = ["<html><head><title>Index</title></head><body>"]
        html.append("<h1>Individuals</h1>")
        html.append("<ul>")
        
        for individual in self.individuals:
            html.append(f'<li><a href="{uri_to_filename(str(individual))}">{escape_html(str(individual))}</a></li>')
        
        html.append("</ul>")
        html.append("</body></html>")
        
        return "\n".join(html)

    def save(self, output_dir="docs"):
        """Saves the index HTML page."""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        with open(f"{output_dir}/index.html", "w") as f:
            f.write(self.render())
        print(f"✅ Saved index page to {output_dir}/index.html")