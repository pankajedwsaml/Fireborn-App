from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)


quotes = {

    "Study": [
        "Small progress is still progress.",
        "Discipline beats motivation.",
        "Study now. Lead later."
    ],

    "Gym": [
        "Pain builds power.",
        "One more rep changes you.",
        "Strong body. Strong mind."
    ],

    "Life": [
        "Growth is uncomfortable.",
        "Keep moving.",
        "Hard times shape legends."
    ],

    "Fireborn": [
        "Born weak. Built in fire.",
        "A king is forged.",
        "Fire never asks permission."
    ]

}



@app.route('/')
def home():
    return render_template("index.html")



@app.route('/random_quote/<category>')
def random_quote(category):

    if category in quotes:

        return jsonify({
            "category": category,
            "quote": random.choice(
                quotes[category]
            )
        })

    return jsonify({})



@app.route('/all_quotes/<category>')
def all_quotes(category):

    data = []


    if category in quotes:

        for q in quotes[category]:

            data.append(
                category + "|" + q
            )


    return jsonify(data)



@app.route('/add_quote', methods=["POST"])
def add_quote():

    data = request.json


    quotes[
        data["category"]
    ].append(
        data["quote"]
    )


    return jsonify({
        "status": "saved"
    })



@app.route('/delete_quote', methods=["POST"])
def delete_quote():

    data = request.json


    if data["quote"] in quotes[data["category"]]:

        quotes[
            data["category"]
        ].remove(
            data["quote"]
        )


    return jsonify({
        "status": "deleted"
    })



if __name__ == "__main__":
    app.run(debug=True)