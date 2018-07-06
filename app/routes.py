from flask import render_template, request, redirect
from app.models import Card
from app import app, db
import random

@app.route("/")
def index():
    try:
        record = random.choice(Card.query.all())
    except:
        record = None
    return render_template("index.html", card=record)

@app.route("/cards/new", methods=["GET", "POST"])
def new_card():
    if request.method == "GET":
        return render_template("new.html")
    else:
        question = request.form["question"]
        topic = request.form["topic"]
        
        card = Card(question, topic)
        db.session.add(card)
        db.session.commit()

        return redirect("/")

@app.route("/cards")
def show_cards():
    return render_template("cards.html")

@app.route("/cards/<int:card_id>")
def get_card(card_id):
    card = Card.query.get(card_id)
    return render_template("show.html", card=card)

@app.route("/cards/<int:card_id>", methods=["POST"])
def edit(card_id):
    print("here!!")
    card = Card.query.get(card_id)
    card.question = request.form["question"]
    card.topic = request.form["topic"]
    
    db.session.commit()
    return redirect("/")

@app.route("/cards/<int:card_id>/delete", methods=["POST"])
def delete_card(card_id):
    Card.query.filter_by(id=card_id).delete()
    db.session.commit()
    return redirect("/")