# tests/test_entity_model.py

import pytest
from rdflib import Graph, URIRef, Namespace, Literal
from src.entity_model import Entity

EX = Namespace("http://example.org/")


@pytest.fixture
def sample_graph():
    g = Graph()
    g.add((URIRef("https://w3id.org/changes/4/aldrovandi/pip/foo/1"), EX.type, EX.Type))
    g.add((URIRef("https://w3id.org/changes/4/aldrovandi/pip/foo/1"), EX.label, Literal("Entity One")))
    g.add((URIRef("https://w3id.org/changes/4/aldrovandi/pip/foo/1"), EX.relatedTo, URIRef("https://w3id.org/changes/4/aldrovandi/pip/foo/2")))
    g.add((URIRef("https://w3id.org/changes/4/aldrovandi/pip/foo/2"), EX.relatedTo, URIRef("https://w3id.org/changes/4/aldrovandi/pip/foo/1")))
    g.add((URIRef("https://w3id.org/changes/4/aldrovandi/pip/foo/2"), EX.label, Literal("Entity Two")))
    return g

def test_entity_init_and_predicate_object(sample_graph):
    entity = Entity(URIRef("https://w3id.org/changes/4/aldrovandi/pip/foo/1"), sample_graph)
    po = entity.get_predicates_objects()

    assert (EX.type, EX.Type) in po
    assert (EX.label, Literal("Entity One")) in po
    assert (EX.relatedTo, URIRef("https://w3id.org/changes/4/aldrovandi/pip/foo/2")) in po
    assert len(po) == 3


def test_entity_subject_predicate(sample_graph):
    entity = Entity(URIRef("https://w3id.org/changes/4/aldrovandi/pip/foo/1"), sample_graph)
    sp = entity.get_subjects_predicates()

    assert (URIRef("https://w3id.org/changes/4/aldrovandi/pip/foo/2"), EX.relatedTo) in sp
    assert len(sp) == 1


def test_related_entities(sample_graph):
    entity = Entity(URIRef("https://w3id.org/changes/4/aldrovandi/pip/foo/1"), sample_graph)
    related = entity.get_related_entities()

    assert URIRef("https://w3id.org/changes/4/aldrovandi/pip/foo/2") in related
    assert URIRef("https://w3id.org/changes/4/aldrovandi/pip/foo/1") not in related


def test_subgraph_extraction(sample_graph):
    entity = Entity(URIRef("https://w3id.org/changes/4/aldrovandi/pip/foo/1"), sample_graph)
    subg = entity.get_entity_subgraph()

    assert len(subg) == 4
    assert (URIRef("https://w3id.org/changes/4/aldrovandi/pip/foo/1"), EX.type, EX.Type) in subg
    assert (URIRef("https://w3id.org/changes/4/aldrovandi/pip/foo/2"), EX.relatedTo, URIRef("https://w3id.org/changes/4/aldrovandi/pip/foo/1")) in subg