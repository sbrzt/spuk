from dataclasses import dataclass
from typing import List, Optional
from rdflib import Graph

@dataclass
class PropertyValuePair:
    property_label: str
    property_uri: str
    value: str
    internal_value: None
    is_literal: bool = False
    is_internal: bool = False

@dataclass
class EntityData:
    uri: str
    types: List[str]
    properties: List[PropertyValuePair]
    snippet: Graph