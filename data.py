"""
data.py - НАБІР ДАНИХ: книги, автори, видавництва, жанри і країни.
Тут тільки дані (словники). Тут немає коду, який будує граф.

Джерела: лише англомовні, французькі та німецькі видання і загальновідомі
факти про них (рік першого видання, видавець, країна видавця, національність автора).
Російських джерел і російських творів у наборі немає.

Щоб додати нову книгу, допишіть рядок у BOOKS.
Щоб додати автора, допишіть рядок у PERSONS.
"""

# Країни: код -> (назва англійською, назва українською, QID у Wikidata)
COUNTRIES = {
    "country-uk": ("United Kingdom", "Велика Британія", "Q145"),
    "country-usa": ("United States", "США", "Q30"),
    "country-france": ("France", "Франція", "Q142"),
    "country-belgium": ("Belgium", "Бельгія", "Q31"),
    "country-germany": ("Germany", "Німеччина", "Q183"),
    "country-czechia": ("Czech Republic", "Чехія", "Q213"),
}

# Видавництва: код -> (назва, код країни)
PUBLISHERS = {
    "publisher-secker-warburg": ("Secker & Warburg", "country-uk"),
    "publisher-thomas-egerton": ("Thomas Egerton", "country-uk"),
    "publisher-american-publishing": ("American Publishing Company", "country-usa"),
    "publisher-webster": ("Charles L. Webster and Company", "country-usa"),
    "publisher-lacroix-verboeckhoven": ("A. Lacroix, Verboeckhoven et Cie", "country-belgium"),
    "publisher-die-schmiede": ("Die Schmiede", "country-germany"),
    "publisher-kurt-wolff": ("Kurt Wolff Verlag", "country-germany"),
}

# Жанри: код -> (назва англійською, назва українською)
GENRES = {
    "genre-dystopia": ("Dystopia", "Антиутопія"),
    "genre-satire": ("Satire", "Сатира"),
    "genre-romance": ("Romance", "Любовний роман"),
    "genre-historical-fiction": ("Historical fiction", "Історичний роман"),
    "genre-modernism": ("Modernism", "Модернізм"),
    "genre-adventure": ("Adventure", "Пригодницька проза"),
}

# Автори: код -> (ім'я, рік народження, код країни, QID у Wikidata)
PERSONS = {
    "person-george-orwell": ("George Orwell", 1903, "country-uk", "Q3335"),
    "person-jane-austen": ("Jane Austen", 1775, "country-uk", "Q36322"),
    "person-franz-kafka": ("Franz Kafka", 1883, "country-czechia", "Q905"),
    "person-mark-twain": ("Mark Twain", 1835, "country-usa", "Q7245"),
    "person-victor-hugo": ("Victor Hugo", 1802, "country-france", "Q535"),
}

# Книги: код -> (назва, мова, рік, код автора, код видавництва, код жанру)
BOOKS = {
    "book-1984": ("Nineteen Eighty-Four", "en", 1949, "person-george-orwell", "publisher-secker-warburg", "genre-dystopia"),
    "book-animal-farm": ("Animal Farm", "en", 1945, "person-george-orwell", "publisher-secker-warburg", "genre-satire"),
    "book-pride-and-prejudice": ("Pride and Prejudice", "en", 1813, "person-jane-austen", "publisher-thomas-egerton", "genre-romance"),
    "book-sense-and-sensibility": ("Sense and Sensibility", "en", 1811, "person-jane-austen", "publisher-thomas-egerton", "genre-romance"),
    "book-the-trial": ("Der Process", "de", 1925, "person-franz-kafka", "publisher-die-schmiede", "genre-modernism"),
    "book-the-metamorphosis": ("Die Verwandlung", "de", 1915, "person-franz-kafka", "publisher-kurt-wolff", "genre-modernism"),
    "book-tom-sawyer": ("The Adventures of Tom Sawyer", "en", 1876, "person-mark-twain", "publisher-american-publishing", "genre-adventure"),
    "book-huckleberry-finn": ("Adventures of Huckleberry Finn", "en", 1884, "person-mark-twain", "publisher-webster", "genre-satire"),
    "book-les-miserables": ("Les Misérables", "fr", 1862, "person-victor-hugo", "publisher-lacroix-verboeckhoven", "genre-historical-fiction"),
}
