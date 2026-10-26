import math
from flask import Flask, jsonify, request, render_template
from werkzeug.exceptions import BadRequest
from recommender import recommend, get_close_titles

app = Flask(__name__)

PRODUCTS = [
    {"id": 1, "nazwa": "Klawiatura mechaniczna", "kategoria": "akcesoria", "cena": 349.99, "opis": "Przełączniki hot-swap, podświetlenie RGB"},
    {"id": 2, "nazwa": "Mysz bezprzewodowa", "kategoria": "akcesoria", "cena": 129.00, "opis": "Ciche przyciski, 4000 DPI"},
    {"id": 3, "nazwa": "Monitor 27 cali", "kategoria": "monitory", "cena": 1099.00, "opis": "Matryca IPS, 144 Hz"},
    {"id": 4, "nazwa": "Słuchawki nauszne", "kategoria": "audio", "cena": 449.00, "opis": "ANC, 40 h pracy na baterii"},
    {"id": 5, "nazwa": "Hub USB-C", "kategoria": "akcesoria", "cena": 199.00, "opis": "HDMI, 3x USB-A, czytnik SD"},
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/api/products")
def products():
    max_price = request.args.get("max_price", type=float)

    if "max_price" in request.args:
        if (max_price is None or max_price < 0 or math.isnan(max_price) or math.isinf(max_price)): return jsonify({"error": "invalid max_price"}), 400
        else:
            filtered_products = []
            for p in PRODUCTS:
                if (p["cena"] <= max_price):
                    filtered_products.append(p)
            return jsonify(filtered_products)

    return jsonify(PRODUCTS)

@app.route("/api/products/<int:product_id>")
def product(product_id):
    for p in PRODUCTS:
        if p["id"] == product_id:
            return jsonify(p)
    return jsonify({"error": "not found"}), 404

@app.route("/api/products", methods=["POST"])
def create_product():
    if not request.is_json: return jsonify({"error": "invalid JSON"}), 400

    try:
        product_data = request.get_json()
    except BadRequest:
        return jsonify({"error": "invalid JSON"}), 400

    if not(isinstance(product_data, dict)): return jsonify({"error": "expected JSON object"}), 400

    if "id" in product_data: return jsonify({"error": "ID is assigned by server"}), 400

    required_keys = ["nazwa", "kategoria", "cena", "opis"]
    if not all(key in product_data for key in required_keys): return jsonify({"error": "expected nazwa, kategoria, cena, opis in JSON"}), 400

    string_keys = ("nazwa", "kategoria", "opis")
    if any(not isinstance(product_data[key], str) or not product_data[key].strip() for key in string_keys): return jsonify({"error": "fields must be non-empty strings"}), 400

    price = product_data["cena"]
    if type(price) not in (int, float) or (type(price) is float and not math.isfinite(price)) or price < 0: return jsonify({"error": "invalid value of cena"}), 400

    max_id = 0
    for p in PRODUCTS:
        if p["id"] > max_id: max_id = p["id"]

    max_id = max_id + 1

    new_product = {"id": max_id, "nazwa": product_data["nazwa"], "kategoria": product_data["kategoria"], "cena": product_data["cena"], "opis": product_data["opis"]}

    PRODUCTS.append(new_product)
    return jsonify(new_product), 201

@app.route("/api/recommend")
def api_recommend():
    title = request.args.get("title", "").strip()
    if not title: return jsonify({"error": "podaj parametr ?title=..."}), 400

    n = request.args.get("top_n", type=int) if "top_n" in request.args else 5
    if n is None or not 1 <= n <= 10: return jsonify({"error": "top_n musi byc z zakresu 1-10"}), 400

    genre = request.args.get("genre", type=str).strip() if "genre" in request.args else None

    recs = recommend(title, n, genre)
    if recs is None:
        close_titles = get_close_titles(title)
        if close_titles: return jsonify({"error": "Nie znam takiego filmu", "suggestions": close_titles}), 404

        return jsonify({"error": "nie znam takiego filmu"}), 404


    return jsonify({"title": title, "count": len(recs), "recommendations": recs})

if __name__ == "__main__":
    app.run(debug=True, port=5001)