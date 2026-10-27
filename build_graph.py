"""
build_graph.py - ПОБУДОВА ГРАФУ: бере дані з data.py і складає з них трійки.

Трійка - це (ЩО, ЯКА ВЛАСТИВІСТЬ, ЗНАЧЕННЯ). Наприклад:
    (книга 1984, автор, Джордж Орвелл)
Тут ми створюємо всі такі трійки і кладемо їх у граф.
"""
from rdflib import Graph, Literal, RDF, RDFS
from rdflib.namespace import FOAF, OWL, XSD

from config import SCHEMA, EX, ONT, WD, bind_prefixes
from data import COUNTRIES, PUBLISHERS, GENRES, PERSONS, BOOKS


def build_graph() -> Graph:
    g = Graph()
    bind_prefixes(g)

    # 1. Країни
    for code, (en, uk, qid) in COUNTRIES.items():
        s = EX[code]
        g.add((s, RDF.type, SCHEMA.Country))
        g.add((s, SCHEMA.name, Literal(en, lang="en")))
        g.add((s, SCHEMA.name, Literal(uk, lang="uk")))
        g.add((s, OWL.sameAs, WD[qid]))

    # 2. Видавництва
    for code, (name, country) in PUBLISHERS.items():
        s = EX[code]
        g.add((s, RDF.type, SCHEMA.Organization))
        g.add((s, SCHEMA.name, Literal(name)))
        g.add((s, SCHEMA.location, EX[country]))

    # 3. Жанри
    for code, (en, uk) in GENRES.items():
        s = EX[code]
        g.add((s, RDF.type, ONT.Genre))
        g.add((s, RDFS.label, Literal(en, lang="en")))
        g.add((s, RDFS.label, Literal(uk, lang="uk")))

    # 4. Автори
    for code, (name, year, country, qid) in PERSONS.items():
        s = EX[code]
        g.add((s, RDF.type, SCHEMA.Person))
        g.add((s, RDF.type, FOAF.Person))
        g.add((s, SCHEMA.name, Literal(name)))
        g.add((s, FOAF.name, Literal(name)))
        g.add((s, SCHEMA.birthDate, Literal(str(year), datatype=XSD.gYear)))
        g.add((s, SCHEMA.nationality, EX[country]))
        g.add((s, OWL.sameAs, WD[qid]))

    # 5. Книги (зв'язують книгу з автором, видавництвом і жанром)
    for code, (title, lang, year, author, publisher, genre) in BOOKS.items():
        s = EX[code]
        g.add((s, RDF.type, SCHEMA.Book))
        g.add((s, SCHEMA.name, Literal(title, lang=lang)))
        g.add((s, SCHEMA.inLanguage, Literal(lang)))
        g.add((s, SCHEMA.datePublished, Literal(year, datatype=XSD.integer)))
        g.add((s, SCHEMA.author, EX[author]))
        g.add((s, SCHEMA.publisher, EX[publisher]))
        g.add((s, SCHEMA.genre, EX[genre]))

    return g
