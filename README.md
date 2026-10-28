# Intelligent Web Lab

Repozytorium zawiera rozwiązania laboratoriów z przedmiotu dotyczącego inteligentnych systemów informatycznych. Projekt obejmuje tworzenie API w Pythonie oraz implementację systemów rekomendacji filmów.

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

Adres i port zależą od konfiguracji aplikacji.

#### Przykładowe zapytanie

```http
GET /api/products
```

Przykładowa odpowiedź:

```json
[
  {
    "id": 1,
    "nazwa": "Klawiatura mechaniczna",
    "kategoria": "akcesoria",
    "cena": 349.99,
    "opis": "Klawiatura mechaniczna"
  }
]
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

#### Przykładowe zapytanie

```http
GET /api/recommend?title=Inception&top_n=5
```

Przykładowa odpowiedź:

```json
{
  "title": "Inception",
  "count": 1,
  "recommendations": [
    {
      "title": "Przykładowy film",
      "genres": "thriller|drama",
      "rating": 8.1,
      "score": 0.42
    }
  ]
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

#### Przykładowe zapytanie

```http
GET /api/recommend?user=Ania&k=3
```

Przykładowa odpowiedź:

```json
{
  "user": "Ania",
  "count": 1,
  "recommendations": [
    {
      "title": "Przykładowy film",
      "predicted": 4.18,
      "because": ["Celina", "Jacek"]
    }
  ]
}
```

Przykładowe odpowiedzi API mają charakter poglądowy. Rzeczywiste wyniki zależą od danych wejściowych i implementacji danego laboratorium.

## Dane wejściowe

- Lab 1 – przykładowe dane produktów zdefiniowane w aplikacji.
- Lab 2 – plik `movies.csv` zawierający informacje o filmach, w tym tytuły, opisy, gatunki i oceny.
- Lab 3 – plik `ratings.csv` zawierający oceny filmów wystawione przez użytkowników.

## Cel projektu

Celem projektu jest poznanie podstaw tworzenia API w Flask, walidacji danych, przetwarzania danych tabelarycznych oraz implementacji metod podobieństwa i rekomendacji.
