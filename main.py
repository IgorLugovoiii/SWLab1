"""
main.py - ГОЛОВНИЙ ФАЙЛ. Запускайте саме його: python main.py

Він не містить логіки сам, а лише викликає інші файли по черзі:
  1. load_graph     (serialize.py)   - створює або читає books.ttl
  2. print_stats    (stats.py)       - рахує трійки та сутності
  3. draw           (visualize.py)   - малює graph.png
  4. save_all       (serialize.py)   - зберігає у RDF/XML, N-Triples, список трійок
  5. print_entity   (serialize.py)   - показує трійки однієї книги
  6. run_all        (run_queries.py) - виконує SPARQL-запити

Запуск:
    python main.py            звичайний запуск
    python main.py --rebuild  створити граф заново (ручні правки в books.ttl зітруться)
"""
import argparse

from config import EX
from serialize import load_graph, save_all_formats, print_entity_triples
from stats import print_stats
from visualize import draw
from run_queries import run_all_queries


def main() -> None:
    parser = argparse.ArgumentParser(description="Лабораторна №01: RDF та SPARQL")
    parser.add_argument("--rebuild", action="store_true",
                        help="створити граф заново з data.py")
    args = parser.parse_args()

    g = load_graph(rebuild=args.rebuild)   # крок 1
    print_stats(g)                          # крок 2
    draw(g)                                 # крок 2b
    save_all_formats(g)                     # крок 3
    print_entity_triples(g, EX["book-1984"])  # крок 3b
    run_all_queries(g)                      # крок 4 і 5


if __name__ == "__main__":
    main()
