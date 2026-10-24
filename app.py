import math
from flask import Flask, jsonify, request

app = Flask(__name__)

PRODUCTS = [
    {"id": 1, "nazwa": "Klawiatura mechaniczna", "kategoria": "akcesoria", "cena": 349.99, "opis": "Przełączniki hot-swap, podświetlenie RGB"},
    {"id": 2, "nazwa": "Mysz bezprzewodowa", "kategoria": "akcesoria", "cena": 129.00, "opis": "Ciche przyciski, 4000 DPI"},
    {"id": 3, "nazwa": "Monitor 27 cali", "kategoria": "monitory", "cena": 1099.00, "opis": "Matryca IPS, 144 Hz"},
    {"id": 4, "nazwa": "Słuchawki nauszne", "kategoria": "audio", "cena": 449.00, "opis": "ANC, 40 h pracy na baterii"},
    {"id": 5, "nazwa": "Hub USB-C", "kategoria": "akcesoria", "cena": 199.00, "opis": "HDMI, 3x USB-A, czytnik SD"},
]

@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/api/products")
def products():
    max_price = request.args.get("max_price", type=float)

    if "max_price" in request.args:
        if (max_price is None or max_price < 0 or math.isnan(max_price) or math.isinf(max_price)): return jsonify({"error": "Invalid max_price"}), 400
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
    return jsonify({"status": "not found"}), 404

@app.route("/api/products", methods=["POST"])
def create_product():
    product_data = request.get_json()

    max_id = 1
    for p in PRODUCTS:
        if p["id"] > max_id: max_id = p["id"]

    max_id = max_id + 1

    new_product = {"id": max_id, "nazwa": product_data["nazwa"], "kategoria": product_data["kategoria"], "cena": product_data["cena"], "opis": product_data["opis"]}

    PRODUCTS.append(new_product)
    return jsonify(new_product), 201

if __name__ == "__main__":
    app.run(debug=True, port=5001)