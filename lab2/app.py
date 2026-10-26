import math
from flask import Flask, jsonify, request, render_template
from werkzeug.exceptions import BadRequest
from recommender import recommend, get_close_titles

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

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