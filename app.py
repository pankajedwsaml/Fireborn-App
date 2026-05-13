from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(BASE_DIR, "quotes.txt")

def load_quotes():
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            return [q.strip() for q in f.readlines() if q.strip()]
    except FileNotFoundError:
        return []

def save_quote(q):
    with open(FILE, "a", encoding="utf-8") as f:
        f.write(q.strip() + "\n")

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/get_quote')
def get_quote():
    quotes = load_quotes()
    if quotes:
        return jsonify({"quote": random.choice(quotes)})
    return jsonify({"quote": "Add your first quote!"})

@app.route('/add_quote', methods=["POST"])
def add_quote():
    data = request.get_json()
    quote = data.get("quote", "").strip()

    if quote:
        save_quote(quote)

    return jsonify({"status": "saved"})

@app.route('/all_quotes')
def all_quotes():
    return jsonify(load_quotes())

@app.route('/delete_quote', methods=["POST"])
def delete_quote():
    data = request.get_json()
    target = data.get("quote", "").strip()

    quotes = load_quotes()
    updated = [q for q in quotes if q != target]

    with open(FILE, "w", encoding="utf-8") as f:
        for q in updated:
            f.write(q + "\n")

    return jsonify({"status": "deleted"})

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)