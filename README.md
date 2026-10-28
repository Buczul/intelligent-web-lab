# Intelligent Web Lab

Repozytorium zawiera rozwiązania laboratoriów z przedmiotu dotyczącego inteligentnych systemów informatycznych.

## Technologie

- Python 3
- Flask – tworzenie API HTTP
- pandas – przetwarzanie danych tabelarycznych
- scikit-learn – TF-IDF i podobieństwo kosinusowe
- SciPy – operacje na macierzach rzadkich

## Instalacja zależności

Zalecane jest utworzenie i aktywowanie środowiska wirtualnego. Następnie zainstaluj pakiety wymagane przez projekt z pliku `requirements.txt`:

```bash
pip install -r requirements.txt
```

## MODUŁ 0

### Lab 1 – API produktów

Proste REST API umożliwiające zarządzanie listą produktów. Aplikacja udostępnia endpointy do sprawdzania stanu serwera, pobierania listy produktów, wyszukiwania produktu po ID oraz dodawania nowych produktów.

Obsługiwane są parametry zapytań i walidacja danych wejściowych, w tym sprawdzanie poprawności formatu JSON oraz wartości pól produktu.

#### Uruchomienie

Przejdź do katalogu laboratorium 1, w którym znajduje się plik `app.py` i uruchom aplikację:

```bash
python app.py
```

Adres i port zależą od konfiguracji aplikacji. Domyślnie ustalono adres 127.0.0.1 oraz port 5001

#### Zapytania

```http
GET /api/health
```
Przykład: 

`http://127.0.0.1:5001/api/health`

Odpowiedź:

```json
{
  "status": "ok"
}
```

```http
GET /api/products
```
Przykład: 

`http://127.0.0.1:5001/api/products`

Odpowiedź:

```json
[
  {
    "cena": 349.99,
    "id": 1,
    "kategoria": "akcesoria",
    "nazwa": "Klawiatura mechaniczna",
    "opis": "Prze\u0142\u0105czniki hot-swap, pod\u015bwietlenie RGB"
  },
  {
    "cena": 129.0,
    "id": 2,
    "kategoria": "akcesoria",
    "nazwa": "Mysz bezprzewodowa",
    "opis": "Ciche przyciski, 4000 DPI"
  }
]
```

Przykład: 

`http://127.0.0.1:5001/api/products/1`

Odpowiedź:

```json
{
  "cena": 349.99,
  "id": 1,
  "kategoria": "akcesoria",
  "nazwa": "Klawiatura mechaniczna",
  "opis": "Prze\u0142\u0105czniki hot-swap, pod\u015bwietlenie RGB"
}
```

```http
POST /api/products
```
Przykład: 

`curl -X POST http://127.0.0.1:5001/api/products -H "Content-Type: application/json" -d "{\"nazwa\":\"Hub USB-C\",\"kategoria\":\"akcesoria\",\"cena\":79.99,\"opis\":\"Hub USB z czterema portami\"}"  `

Odpowiedź:

```json
{
  "cena": 79.99,
  "id": 6,
  "kategoria": "akcesoria",
  "nazwa": "Hub USB-C",
  "opis": "Hub USB z czterema portami"
}
```

## MODUŁ 1

### Lab 2 – Rekomendacje filmów na podstawie opisów

System rekomendacji wykorzystujący treść opisów filmów do wyszukiwania podobnych tytułów.

Do reprezentacji tekstu wykorzystywana jest metoda TF-IDF, a podobieństwo między filmami obliczane jest za pomocą podobieństwa kosinusowego. API umożliwia uzyskanie rekomendacji dla wskazanego filmu oraz ograniczenie liczby wyników i filtrowanie według gatunku.

#### Uruchomienie

Przejdź do katalogu laboratorium 2, w którym znajduje się plik `app.py` i wymagany plik `movies.csv`, a następnie uruchom:

```bash
python app.py
```

#### INDEX.html

Po uruchomieniu `app.py` pod adresem `http://127.0.0.1:5001/` będzie dostępna prosta strona html z formularzem rekomendacji.

#### Zapytania

```http
GET /api/recommend
```
Przykład: 

`http://127.0.0.1:5001/api/recommend?title=Her&top_n=3&genre=drama`

Parametry `top_n` oraz `genre` są opcjonalne.

Odpowiedź:

```json
{
  "count": 3,
  "recommendations": [
    {
      "genre": "romance|drama",
      "rating": 7.9,
      "score": 0.237,
      "title": "Titanic"
    },
    {
      "genre": "sci-fi|drama",
      "rating": 8.6,
      "score": 0.167,
      "title": "Interstellar"
    },
    {
      "genre": "romance|drama",
      "rating": 7.8,
      "score": 0.167,
      "title": "The Notebook"
    }
  ],
  "title": "Her"
}
```

### Lab 3 – Rekomendacje filmów na podstawie ocen użytkowników

System rekomendacji wykorzystujący oceny wystawione przez użytkowników. Na podstawie macierzy ocen obliczane są średnie użytkowników oraz podobieństwo między nimi. Przewidywane oceny filmów wyznaczane są z wykorzystaniem ocen podobnych użytkowników.

Moduł uwzględnia wybór liczby sąsiadów (`k`), mechanizm zastępczy dla użytkowników z niewielką liczbą ocen oraz analizę podobieństwa filmów na podstawie wzorców ocen. Jakość przewidywań można oceniać za pomocą MAE i pokrycia.

#### Uruchomienie

Przejdź do katalogu laboratorium 3, w którym znajduje się plik `app.py` i wymagany plik `ratings.csv`, a następnie uruchom:

```bash
python app.py
```

#### Zapytania

```http
GET /api/recommend
```

Przykład: 

`http://127.0.0.1:5001/api/recommend?user=Ania&k=3`

Parametr `k` jest opcjonalny.

Odpowiedź:

```json
{
  "count": 5,
  "recommendations": [
    {
      "because": [
        "Celina",
        "Jacek",
        "Kasia"
      ],
      "predicted": 4.31,
      "title": "Fight Club"
    },
    {
      "because": [
        "Celina"
      ],
      "predicted": 3.08,
      "title": "Forrest Gump"
    },
    {
      "because": [
        "Celina",
        "Jacek",
        "Kasia"
      ],
      "predicted": 2.37,
      "title": "Toy Story"
    },
    {
      "because": [
        "Kasia"
      ],
      "predicted": 2.24,
      "title": "The Shawshank Redemption"
    },
    {
      "because": [
        "Celina",
        "Jacek",
        "Kasia"
      ],
      "predicted": 2.13,
      "title": "Spirited Away"
    }
  ],
  "user": "Ania"
}
```

Przykład: 

`http://127.0.0.1:5001/api/recommend?user=Bogdan`

`Bogdan` to użytkownik celowo dodany do bazy z tylko jednym ocenionym filmem.

Odpowiedź:

```json
{
  "count": 5,
  "recommendations": [
    {
      "rate": 4.25,
      "title": "Fight Club"
    },
    {
      "rate": 4.0,
      "title": "The Shawshank Redemption"
    },
    {
      "rate": 3.91,
      "title": "Her"
    },
    {
      "rate": 3.88,
      "title": "A Quiet Place"
    },
    {
      "rate": 3.86,
      "title": "Forrest Gump"
    }
  ],
  "user": "Bogdan"
}
```

## Dane wejściowe

- Lab 1 – przykładowe dane produktów zdefiniowane w aplikacji.
- Lab 2 – plik `movies.csv` zawierający informacje o filmach, w tym tytuły, opisy, gatunki i oceny.
- Lab 3 – plik `ratings.csv` zawierający oceny filmów wystawione przez użytkowników.
