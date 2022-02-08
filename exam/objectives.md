# Serialization
* What is serialization? What is deserialization?
    * Umwandlung von in-memory Objeckten in persistierbare Daten (Serialization) und umgekehrt (Deserialization)
* How can serialization be performed in Python?
    * Json, Pickle, Yaml
* What is Pickle?
    * Implementierung von Serialisierung/Deserialisierung in Python, basierend auf Byte-Streams
* What data-format does Pickle serialize into?
    * Byte-Streams / Binär Dateien
* What are the methods for serialization and deserialization in pickle?
    * pickle.dump(obj, file) / pickle.load(file)
* What are the differences to JSON? 
    * binär, nicht mensch-lesbar, python-spezifisch (dadurch wird auch mehr in python gecovered wie mit JSON)

# Datastorage
* How could data be loaded and stored in Python?
    * txt, csv, json, sql, db, zip, html, ...
    * diverse packete
* Why are text files sometimes still useful?
    * Einfachste Form, sehr verbreitet
    * yaml, html, csv sind auch text-based
* What are the two ways to load text files to Python?
    * f = open(file, mode); f.close()
    * with open(file, mode) as f: //disposable stuff see C# using
* What are the two important Python-json commands?
    * json.dump(data, f)
    * json.load(f)
* Which are the steps to connect to a sqlite3 database?
    * Verbindung aufbauen (conn = sqlite3.connect('example.db'))
    * Curser erstellen (c = conn.cursor())
* What are the two main object in sqlite3?
    * Connection (Verbindung zu Datenbank, Commit, Rollback, Cursorerzeugung)
    * Cursor (Operationen ausführen)

# Numpy
* What is NumPy? Why do we use it?
    * Grundlegendes Packet für wissenschaftliche Berechnungen, sehr performant (wegen c)
* What is the main data type in NumPy?
    * homogene, multidimensionale Arrays
* How can i sort values in Numpy?
    * np.sort(ndarray), ndarray.sort()
* What are two ways to add values column wise in NumPy?
    * np.concatenate(), np.append()
* Which operators are available in Numpy?
    * Sum, Difference, Product
* What does "Shape manipulation" mean?
    * Anzahl der Elemente pro Achse ändern (bzw einfach die shape des ndarrays anpassen, muss aber sich mit den Elementen ausgehen)
* What is the difference between a numpy array and a list?
    * np array => in c, feste Grüßen, gleicher Typ, direkt im Speicher hintereinander
    * list => in python, dynamisch, besteht aus Referenzen
* Name some of the available linear algebra operations in Numpy.
    * Transpose, Inverse, Einheitsmatrix, Matrix product, Eigenwert

# Pandas
* What is Pandas? Benefits.
    * Packet für schnelle, flexible Datenstrukturen
    * Leicht verarbeitbar, große Datenmengen, übersichtliche Darstellung
* How to load and save files in Panda?
    * df = pandas.read_xxx(r'input_file.xxx') 
    * df.to_xxx(r'output_file.xxx')
    * xxx mit konkreten typ ersetzen (zb csv)
* Different Kinds of Datastructures in Pandas?
    * Series -> 1D
    * Dataframe -> 2D
    * beide haben labels und indizes auf den achsen
* Different ways to index in Pandas?
    * loc -> label based (see labels of series and dataframes)
        * label identifies row
        * ```pokemon.loc[['Bulbasaur', 'Ivysaur']]```
    * iloc -> integer based (like normal array/matrix)
         * pokemon.iloc[1:10]
    * [] -> label based Attribut (column)
        * pokemon['Generation']
    * direct attribute (.label) (column)
        * pokemon.Generation
* Difference append() concatenate()? (https://stackoverflow.com/questions/15819050/pandas-dataframe-concat-vs-append)
    * Concat gives the flexibility to join based on the axis( all rows or all columns)
    * Append is the specific case(axis=0, join='outer') of concat
* Which ways of SQL-like transforming do i have in Pandas? 
    * Merge / Join to add two data together
    * groupby() for grouping

# Flask
* What are virtual environments?
    * Keep dependencies required by different projects separate
* What is Flask?
    * Microweb Framework of Python providing tools, libraries and technologies to build a web application
* Basic steps to start with Falsk.
    * form flask Import Flask
    * app = Flask(\_\_name__)
    * if \_\_name__ == '\_\_main__':
        app.run()
* What is routing and how is it in Flask?
    * For binding a specific function to a url
    * @app.route(route)
* What are templates? How to use?
    * html dokumente
    * return render_template('hello.html')
* How are HTTP methods in Flask?
    * add to @app.route => @app.route(route, methods=['POST', 'GET', ...])
* What is Jinja?
    * Template Engine; stellt bindings zur Verfügung
    * eh scho property binding ({{ cock }}, {% if cock.size == 0 %})
    * ```{# comment #} {% statement %} {{ binding }} {{% block placeholder für replacement %}}```
* Database in Flask?
    * SQL Alchemy => mächtiger OR Mapper
    * app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite3'
    * db = SQLAlchemy(app)
    * db.Model erstellen als Klasse

# PyQt5
* What it be?
    * Python Package to make graphical user interfaces
    * UI Framework
    * Based on Qt Widget Toolkit (wrapper / python bindings)
* Main object in PyQt5?
    * Application
    * MainWindow
    * Widgets
* Qt Designer?
    * graphical designer (WYSIWYG), gives a .ui file
    * pyuic5 -x ui_file.ui -o python_file.py (convert to py)

# Web Scraping
* Why is web scraping so easy in python?
    * viele packete die es vereinfachen
    * requests library -> easy requests on a url to get the response (automated processing of response => aufarbeitung des responses)
    * Beatifulsoup library -> parser for that text
* Steps to web scraping?
    * make request on the website
    * parse the result
    * now you can search for tags/elements/properties
* Return instance of request methods?
    * contains all kinds of stuff (like what you see when inspecting http trafic)
    * response object
* What is beautiful soup?
  * Beautiful Soup is a Python library for pulling data out of HTML and XML files. It works with your favorite parser to provide idiomatic ways of navigating, searching, and modifying the parse tree (DOM).
* Some bs4 functions.
    * soup.find_all(tag, {attribute: attribute_value})
    * soup.find(-||-) same as find_all, but only get first appearance
    * soup.find(-||-).get(attribute)
* Difference Tags and attributes
    * Tags -> find/find_all on soup
    * attributes -> get on tag