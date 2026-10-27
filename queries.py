"""
queries.py - SPARQL-ЗАПИТИ: це "питання до графу" мовою SPARQL.

Кожен запит - це питання + текст запиту. Самі запити тут тільки записані,
виконує їх run_queries.py.
"""

# Короткі назви, щоб не писати повні адреси в кожному запиті
PREFIXES = """PREFIX schema: <https://schema.org/>
PREFIX ex: <http://library.example.org/resource/>
PREFIX ont: <http://library.example.org/ontology#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
"""

QUERIES = [
    {
        "id": "Q1",
        "question": "Які книги написав Джордж Орвелл? (сортування за роком)",
        "sparql": """SELECT ?title ?year WHERE {
  ?book schema:author ex:person-george-orwell ;
        schema:name ?title ;
        schema:datePublished ?year .
}
ORDER BY ?year""",
    },
    {
        "id": "Q2",
        "question": "Скільки книг у графі має кожен автор? (COUNT)",
        "sparql": """SELECT ?authorName (COUNT(?book) AS ?n) WHERE {
  ?book schema:author ?author .
  ?author schema:name ?authorName .
}
GROUP BY ?authorName
ORDER BY DESC(?n) ?authorName""",
    },
    {
        "id": "Q3",
        "question": "Які книги видані у Німеччині? (ланцюжок: книга -> видавництво -> країна -> назва, 3 зв'язки)",
        "sparql": """SELECT ?title ?publisherName WHERE {
  ?book schema:name ?title ;
        schema:publisher ?pub .
  ?pub schema:name ?publisherName ;
       schema:location ?country .
  ?country schema:name "Germany"@en .
}
ORDER BY ?title""",
    },
    {
        "id": "Q4",
        "question": "Які книги видані після 1900 року? (FILTER + сортування за спаданням)",
        "sparql": """SELECT ?title ?year WHERE {
  ?book schema:name ?title ;
        schema:datePublished ?year .
  FILTER(?year > 1900)
}
ORDER BY DESC(?year)""",
    },
    {
        "id": "Q5",
        "question": "Перший, останній і середній рік видання для кожного жанру (MIN, MAX, AVG)",
        "sparql": """SELECT ?genreLabel (COUNT(?book) AS ?books) (MIN(?year) AS ?first)
       (MAX(?year) AS ?last) (AVG(?year) AS ?avgYear) WHERE {
  ?book schema:genre ?genre ;
        schema:datePublished ?year .
  ?genre rdfs:label ?genreLabel .
  FILTER(LANG(?genreLabel) = "en")
}
GROUP BY ?genreLabel
ORDER BY ?avgYear""",
    },
    {
        "id": "Q6",
        "question": "Книги, написані авторами з Франції (зв'язок між типами: книга -> автор -> країна)",
        "sparql": """SELECT ?title ?authorName WHERE {
  ?book schema:name ?title ;
        schema:author ?author .
  ?author schema:name ?authorName ;
          schema:nationality ?country .
  ?country schema:name "France"@en .
}
ORDER BY ?authorName ?title""",
    },
]

# ПОМИЛКОВИЙ запит (для звіту): число порівнюємо з рядком у лапках
WRONG_QUERY = {
    "id": "Q4-wrong",
    "question": "ПОМИЛКА: FILTER порівнює рік (число) з рядком \"1900\"",
    "sparql": """SELECT ?title ?year WHERE {
  ?book schema:name ?title ;
        schema:datePublished ?year .
  FILTER(?year > "1900")
}
ORDER BY DESC(?year)""",
}

# Той самий запит, виправлений: лапки прибрано
FIXED_QUERY = {
    "id": "Q4-fixed",
    "question": "ВИПРАВЛЕНО: FILTER(?year > 1900) без лапок",
    "sparql": WRONG_QUERY["sparql"].replace('"1900"', "1900"),
}

# Запит до Wikidata (потрібен інтернет). Поєднує наш граф і Wikidata.
FEDERATED_QUERY = {
    "id": "Q7-federated",
    "question": "Зв'язок із Wikidata: український підпис і дата народження автора з Wikidata",
    "sparql": """SELECT ?authorName ?wd ?wdLabel ?wdBirth WHERE {
  ?author a schema:Person ;
          schema:name ?authorName ;
          owl:sameAs ?wd .
  FILTER(STRSTARTS(STR(?wd), "http://www.wikidata.org/entity/"))
  SERVICE <https://query.wikidata.org/sparql> {
    ?wd rdfs:label ?wdLabel .
    FILTER(LANG(?wdLabel) = "uk")
    OPTIONAL { ?wd wdt:P569 ?wdBirth . }
  }
}
ORDER BY ?authorName""",
}
