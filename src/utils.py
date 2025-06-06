import html, os, tomllib
from urllib.parse import urlparse

with open("config.toml", "rb") as f:
    configuration = tomllib.load(f)

GITHUB_DEPLOY = configuration["general"]["github_deploy"]
REPO_NAME = configuration["general"]["repo_name"]
ROOT_DIR = configuration["general"]["root_dir"]


def get_uri_label(uri: str) -> str:
    if "#" in uri:
        return uri.split("#")[-1]
    return uri.rstrip("/").split("/")[-1]

def escape_html(text: str) -> str:
    return html.escape(text)

def uri_to_filename(uri: str) -> str:
    path = urlparse(uri).path
    path = path.replace("#", "/")
    filename = path.strip("/").split("/")[-1]
    return filename

def get_namespace(uri: str) -> str:
    if "#" in uri:
        return uri.rsplit("#", 1)[0] + "#"
    return uri.rsplit("/", 1)[0] + "/"

def remove_root(path):
    if configuration["general"]["github_deploy"]:
        return f"/{REPO_NAME}/" + "/".join(path.split("/")[1:])
    else:
        return "/" + "/".join(path.split("/")[1:])

def generate_path(uri):
    path = urlparse(uri).path
    parts = path.strip("/").split("/")[:-1]
    full_path = os.path.join(ROOT_DIR, *parts)
    return full_path

def generate_base_path(path):
    folder = os.path.dirname(path) or "."
    relative = os.path.relpath(folder, ROOT_DIR)
    if relative == ".":
        return ""
    parts = relative.split(os.sep)
    depth = len(parts)
    return "../" * depth