"""
config.py - НАЛАШТУВАННЯ: шляхи до файлів і простори імен (адреси словників).
Цей файл ніхто не запускає сам. Його імпортують інші файли.
"""
import os
import sys

from rdflib import Graph, Namespace, RDFS
from rdflib.namespace import FOAF, OWL

# Щоб українські символи коректно друкувались у консолі Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Папка, де лежить цей файл. Усі результати зберігаються тут.
HERE = os.path.dirname(os.path.abspath(__file__))

# Усі результати програми йдуть у окрему папку output
OUT = os.path.join(HERE, "output")
os.makedirs(OUT, exist_ok=True)

TTL = os.path.join(OUT, "books.ttl")                   # основний файл Turtle
RDFXML = os.path.join(OUT, "books.rdf")                # той самий граф у RDF/XML
NT = os.path.join(OUT, "books.nt")                     # той самий граф у N-Triples
TRIPLES_TXT = os.path.join(OUT, "triples_all.txt")     # усі трійки списком
PNG = os.path.join(OUT, "graph.png")                   # картинка графу
RESULTS_TXT = os.path.join(OUT, "results.txt")         # результати SPARQL

# Простори імен (адреси словників і наших ресурсів)
SCHEMA = Namespace("https://schema.org/")                # готовий словник schema.org
EX = Namespace("http://library.example.org/resource/")   # НАШІ URI ресурсів
ONT = Namespace("http://library.example.org/ontology#")  # наш клас Genre
WD = Namespace("http://www.wikidata.org/entity/")        # Wikidata


def bind_prefixes(g: Graph) -> None:
    """Задає короткі назви префіксів (schema:, ex: ...) для графу."""
    g.bind("schema", SCHEMA)
    g.bind("ex", EX)
    g.bind("ont", ONT)
    g.bind("foaf", FOAF)
    g.bind("owl", OWL)
    g.bind("rdfs", RDFS)
    g.bind("wd", WD)
