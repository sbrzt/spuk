import html
from urllib.parse import urlparse


def get_uri_label(uri: str) -> str:
    """Extracts the last fragment or path segment of a URI."""
    if "#" in uri:
        return uri.split("#")[-1]
    return uri.rstrip("/").split("/")[-1]

def escape_html(text: str) -> str:
    """Escape special characters in text for safe HTML output."""
    return html.escape(text)

def uri_to_filename(uri: str) -> str:
    """Convert a URI into a valid HTML filename (strip protocol and fragments)."""
    return uri.strip().split('/')[-1].replace('#', '_') + ".html"


