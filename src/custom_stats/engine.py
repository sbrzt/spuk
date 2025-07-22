# src/custom_stats/engine.py

from config import STATS_CONFIG
import yaml
from rdflib import URIRef
from .registry import STAT_TYPES


def load_custom_stats(graph, config_path=STATS_CONFIG):
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    custom_stats = {}
    for item in config.get("custom_stats", []):
        name = item["name"]
        label = item.get("label", name)
        stat_type = item["type"]
        predicate = URIRef(item["predicate"])
        func = STAT_TYPES.get(stat_type)

        if func:
            result = func(graph, predicate)
            custom_stats[name] = {
                "label": label,
                "data": result
            }
    return custom_stats
