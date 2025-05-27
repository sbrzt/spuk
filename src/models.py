from dataclasses import dataclass
from typing import List, Optional
from rdflib import Graph

@dataclass
class PropertyValuePair:
    property_label: str
    property_uri: str
    value: str
    is_literal: bool = False

@dataclass
class EntityData:
    uri: str
    types: List[str]
    properties: List[PropertyValuePair]
    snippet: Graph