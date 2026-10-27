"""
visualize.py - ВІЗУАЛІЗАЦІЯ: малює граф як картинку graph.png.

Вузли - це сутності (книги, автори, ...), стрілки - це зв'язки.
Колір вузла показує його тип.
"""
import networkx as nx
import matplotlib

matplotlib.use("Agg")  # малювати у файл, без вікна
import matplotlib.pyplot as plt  # noqa: E402
from rdflib import Graph, RDF, RDFS

from config import SCHEMA, ONT, PNG

TYPE_NAMES = {
    SCHEMA.Book: "Book",
    SCHEMA.Person: "Person",
    SCHEMA.Organization: "Organization",
    SCHEMA.Country: "Country",
    ONT.Genre: "Genre",
}
TYPE_COLORS = {
    "Book": "#4C78A8",
    "Person": "#F58518",
    "Organization": "#54A24B",
    "Genre": "#B279A2",
    "Country": "#E45756",
}
LINK_PREDICATES = {SCHEMA.author, SCHEMA.genre, SCHEMA.publisher,
                   SCHEMA.nationality, SCHEMA.location}


def _node_name(g: Graph, node) -> str:
    """Знаходить людську назву вузла (спочатку англійську)."""
    names = list(g.objects(node, SCHEMA.name)) + list(g.objects(node, RDFS.label))
    for lit in names:
        if getattr(lit, "language", None) == "en":
            return str(lit)
    if names:
        return str(names[0])
    return str(node).split("/")[-1]


def draw(g: Graph) -> None:
    # 1. Знаходимо всі сутності та їх тип
    G = nx.DiGraph()
    node_type = {}
    for s in set(g.subjects(RDF.type, None)):
        for t in g.objects(s, RDF.type):
            if t in TYPE_NAMES:
                node_type[s] = TYPE_NAMES[t]

    # 2. Додаємо вузли та зв'язки між ними
    for s, kind in node_type.items():
        G.add_node(s, label=_node_name(g, s), kind=kind)
    for s, p, o in g:
        if p in LINK_PREDICATES and s in node_type and o in node_type:
            G.add_edge(s, o, label=p.split("/")[-1])

    # 3. Розміщуємо вузли і малюємо
    pos = nx.spring_layout(G, seed=7, k=2.2, iterations=300)
    plt.figure(figsize=(16, 11))
    for kind, color in TYPE_COLORS.items():
        nodes = [n for n in G.nodes if G.nodes[n]["kind"] == kind]
        nx.draw_networkx_nodes(G, pos, nodelist=nodes, node_color=color,
                               node_size=900, alpha=0.9, label=kind)
    nx.draw_networkx_edges(G, pos, arrows=True, arrowsize=14,
                           edge_color="#999999", width=1.2, node_size=900)
    nx.draw_networkx_labels(G, pos, labels={n: G.nodes[n]["label"] for n in G.nodes},
                            font_size=7)
    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels={(u, v): d["label"] for u, v, d in G.edges(data=True)},
        font_size=6, font_color="#555555")
    plt.title("Граф знань: книги, автори, видавництва, жанри, країни", fontsize=14)
    plt.legend(loc="upper left", fontsize=9, markerscale=0.4)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(PNG, dpi=150)
    plt.close()
    print(f"\n[2b] Картинку збережено: {PNG} "
          f"(вузлів: {G.number_of_nodes()}, зв'язків: {G.number_of_edges()})")
