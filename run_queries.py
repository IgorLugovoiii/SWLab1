"""
run_queries.py - ВИКОНАННЯ ЗАПИТІВ: запускає SPARQL-запити з queries.py
на нашому графі і показує результати (і пише їх у results.txt).
"""
from rdflib import Graph

from config import RESULTS_TXT
from queries import PREFIXES, QUERIES, WRONG_QUERY, FIXED_QUERY, FEDERATED_QUERY


def run_query(g: Graph, item: dict, out) -> None:
    """Виконує один запит і виводить його текст та результат."""
    header = f"\n=== {item['id']}: {item['question']}"
    print(header)
    print(item["sparql"])
    out.write(header + "\n" + item["sparql"] + "\n")
    try:
        res = g.query(PREFIXES + item["sparql"])
        rows = [" | ".join("" if v is None else str(v) for v in row) for row in res]
        cols = " | ".join(str(v) for v in res.vars)
        line = f"-- Результат ({len(rows)} рядків): {cols}"
        print(line)
        out.write(line + "\n")
        for r in rows:
            print("   " + r)
            out.write("   " + r + "\n")
        if not rows:
            print("   (порожньо)")
            out.write("   (порожньо)\n")
    except Exception as e:  # noqa: BLE001 - показуємо будь-яку помилку
        msg = f"-- Помилка виконання: {e}"
        print(msg)
        out.write(msg + "\n")


def run_all_queries(g: Graph) -> None:
    print("\n[4] SPARQL-запити до нашого графу")
    with open(RESULTS_TXT, "w", encoding="utf-8") as out:
        for item in QUERIES:
            run_query(g, item, out)

        print("\n[4b] Помилковий і виправлений приклад (для звіту, п. 6)")
        out.write("\n### Помилковий та виправлений приклад\n")
        run_query(g, WRONG_QUERY, out)
        run_query(g, FIXED_QUERY, out)

        print("\n[5] Федеративний запит до Wikidata (потрібен інтернет)")
        out.write("\n### Федеративний запит до Wikidata\n")
        run_query(g, FEDERATED_QUERY, out)

    print("\nУсі результати записано у output")
