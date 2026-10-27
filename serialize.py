"""
serialize.py - ЗБЕРЕЖЕННЯ І ЧИТАННЯ ГРАФУ У ФАЙЛИ.

Граф у пам'яті зникає, коли програма завершилась. Тому ми записуємо його у файли:
  - books.ttl  (Turtle, людський формат, його можна редагувати руками)
  - books.rdf  (RDF/XML, ще один формат)
  - books.nt   (N-Triples, найпростіший формат: одна трійка в одному рядку)
  - triples_all.txt (усі трійки списком)
"""
import os

from rdflib import Graph

from config import TTL, RDFXML, NT, TRIPLES_TXT, bind_prefixes
from build_graph import build_graph


def load_graph(rebuild: bool) -> Graph:
    """
    Якщо books.ttl немає (або ввімкнено rebuild) - створює його з data.py.
    Інакше читає books.ttl, тож ваші ручні правки зберігаються.
    """
    if rebuild or not os.path.exists(TTL):
        g = build_graph()
        g.serialize(destination=TTL, format="turtle", encoding="utf-8")
        print(f"[1] Граф створено з data.py і збережено у {TTL}")
    else:
        print(f"[1] Читаю існуючий {TTL} (ручні правки збережено)")

    g = Graph()
    bind_prefixes(g)
    g.parse(TTL, format="turtle")
    return g


def save_all_formats(g: Graph) -> None:
    """Зберігає граф у RDF/XML, N-Triples і текстовий список трійок."""
    g.serialize(destination=RDFXML, format="xml", encoding="utf-8")
    g.serialize(destination=NT, format="nt", encoding="utf-8")
    with open(TRIPLES_TXT, "w", encoding="utf-8") as f:
        for s, p, o in sorted(g, key=lambda t: (str(t[0]), str(t[1]), str(t[2]))):
            f.write(f"{s.n3(g.namespace_manager)} {p.n3(g.namespace_manager)} "
                    f"{o.n3(g.namespace_manager)} .\n")
    print(f"[3] Збережено: RDF/XML -> {RDFXML}")
    print(f"              N-Triples -> {NT}")
    print(f"              усі трійки -> {TRIPLES_TXT}")


def print_entity_triples(g: Graph, entity) -> None:
    """Виводить на екран усі трійки, пов'язані з однією сутністю."""
    nm = g.namespace_manager
    print(f"\n[3] Трійки, пов'язані з {entity.n3(nm)}:")
    print("    Де він суб'єкт (про що твердження):")
    for _, p, o in g.triples((entity, None, None)):
        print(f"      {p.n3(nm)}  {o.n3(nm)}")
    print("    Де він об'єкт (хто на нього посилається):")
    for s, p, _ in g.triples((None, None, entity)):
        print(f"      {s.n3(nm)}  {p.n3(nm)}")
