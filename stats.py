"""
stats.py - СТАТИСТИКА: скільки трійок, сутностей і типів зв'язків у графі.
Потрібно, щоб перевірити вимоги завдання (5 типів, 20+ екземплярів, 50+ трійок).
"""
from rdflib import Graph, Literal, RDF

from config import SCHEMA, ONT


def print_stats(g: Graph) -> None:
    types = {
        SCHEMA.Book: "Book",
        SCHEMA.Person: "Person",
        SCHEMA.Organization: "Organization",
        SCHEMA.Country: "Country",
        ONT.Genre: "Genre",
    }
    print("\n[2] Структура графу")
    print(f"    Усього трійок: {len(g)}")
    for t, label in types.items():
        print(f"    Тип {label:13s}: {len(set(g.subjects(RDF.type, t)))} екземплярів")

    # Типи зв'язків: властивості, де значення - це посилання на інший ресурс
    obj_preds = {p for _, p, o in g if not isinstance(o, Literal) and p != RDF.type}
    print(f"    Типів зв'язків: {len(obj_preds)}")
    for p in sorted(obj_preds, key=str):
        print(f"      - {g.namespace_manager.normalizeUri(p)}")
