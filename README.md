Ta aplikacja jest internetową aplikacją do zarządzania projektami. Główne funkcje tej aplikacji internetowej obejmują
Dodawanie projektów: Użytkownik może dodać nowy projekt poprzez wprowadzenie nazwy projektu.
Dodawanie kamieni milowych do projektów: Po utworzeniu projektu użytkownik może dodać do niego kamienie milowe.
Usuwanie projektów i etapów: Użytkownik może usunąć projekt jako całość lub poszczególne etapy.
Zmiana statusu etapów: Użytkownik może przełączać status etapów pomiędzy "ukończony" i "nieukończony".
Wyświetlanie listy projektów i ich etapów: Wszystkie projekty i ich etapy są wyświetlane na stronie głównej aplikacji internetowej.
W ten sposób aplikacja umożliwia użytkownikom tworzenie, zarządzanie i śledzenie postępów różnych projektów, zapewniając możliwość dodawania etapów i zmiany ich statusu w wygodny sposób za pośrednictwem interfejsu internetowego.
aplikacja została napisana przy użyciu języka programowania python oraz bibliotek flask mongoclient i bson
jako część backendu.
W pliku main.py z biblioteki Flask importujemy samego Flaska, render template - mówimy naszemu programowi jak ma coś wyrenderować, request to żądanie, które przyszło do nas w danym momencie, redirect to przekierowanie do jakiegoś miejsca, url_for to lista wszystkich funkcji, które mamy, nazywa się to również endpoint, aby można je było następnie wykorzystać we Flasku do przekierowania użytkownika na inną stronę.
Pymongo dla Pythona do pracy z witryną mongodb.com, gdzie znajduje się nasza baza danych. W module bson biblioteki PyMongo funkcja ObjectId służy do tworzenia unikalnych identyfikatorów obiektów w bazie danych MongoDB. Każdy dokument w MongoDB ma unikalny identyfikator zwany ObjectId.
Następnie uruchamiamy Flask używając naszej nazwy: app = Flask(__name__)
następnie łączymy się z klastrem mongodb:client = MongoClient('mongodb+srv://maksvin1111:6Ndfv4XtVYw9ax33@cluster0.cnm3lns.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
Następnie znajdujemy lub tworzymy menedżera projektu w klastrze :db = client['project_manager'].
Wewnątrz menedżera projektów tworzymy kolekcję projektów:projects_collection = db['projects']

Główny punkt końcowy (strona główna), kiedy do niego przechodzimy, ładujemy przez .find()
  z mondodb wszystkie projekty, które mamy i renderujemy je przez index.html:
@app.route('/')
def index():
    projects = projects_collection.find()
    return render_template('index.html', projects=projects)

Następnie mamy:
Ta funkcja dodaje nowy projekt do bazy danych po otrzymaniu żądania POST na trasie /add_project.
Główne działania funkcji:
@app.route('/add_project', methods=['POST'])
def add_project():
    name = request.form['name']
    project = {'name': 'name', 'stages': []}
    projects_collection.insert_one(project)
    return redirect(url_for('index'))

Ta funkcja dodaje nowy projekt do bazy danych po otrzymaniu żądania POST na trasie /add_project.
Główne działania funkcji:
Pobieranie nazwy nowego projektu z danych formularza przesłanych przez użytkownika.
Utworzenie słownika projektu zawierającego dane nowego projektu: nazwę projektu i pustą listę etapów.
Dodanie tego słownika do kolekcji projects_collection bazy danych MongoDB przy użyciu metody insert_one().
Po pomyślnym dodaniu projektu funkcja przekierowuje użytkownika na stronę główną aplikacji za pomocą funkcji redirect(url_for('index')), gdzie index to nazwa funkcji odpowiedzialnej za stronę główną aplikacji.

Po pomyślnym dodaniu projektu funkcja przekierowuje użytkownika na stronę główną aplikacji za pomocą funkcji redirect(url_for('index')), gdzie index to nazwa funkcji odpowiedzialnej za stronę główną aplikacji.




@app.route('/add_stage/<project_id>', methods=['POST'])
def add_stage(project_id):
    stage_name = request.form['stage_name'].
    projects_collection.update_one(
        { "_id": ObjectId(project_id)}
        {"$push": {"stages": {"name": stage_name, "status": 'not completed'}}

Ta funkcja wykonuje dodanie nowego etapu do określonego projektu w bazie danych po otrzymaniu żądania POST na trasie /add_stage/<project_id>.
Główne działania funkcji:
Pobranie nazwy nowego etapu z danych formularza przesłanych przez użytkownika.
Aktualizacja dokumentu projektu w kolekcji projects_collection bazy danych MongoDB przy użyciu metody update_one().
Określenie warunku wyszukiwania dokumentu na podstawie jego _id, który jest przekazywany jako parametr project_id.
Użycie operatora $push w celu dodania nowego etapu do tablicy etapów projektu.
Utworzenie nowego obiektu stage z nazwą otrzymaną z formularza i statusem "not completed".
Po pomyślnym zaktualizowaniu dokumentu projektu funkcja kończy działanie.


@app.route('/delete_project/<project_id>')
def delete_project(project_id):
    projects_collection.delete_one({'_id': ObjectId(project_id)})
    return redirect(url_for('index'))

Ta funkcja usuwa projekt z bazy danych po otrzymaniu żądania GET na trasie /delete_project/<project_id>.
Główne działania funkcji:
Pobranie identyfikatora projektu z adresu URL, który jest przekazywany jako parametr project_id.
Użycie metody delete_one() do usunięcia dokumentu projektu z kolekcji projektów.
