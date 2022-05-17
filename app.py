from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from random import randint


app = Flask(__name__)
app.config["SQLALCHEMY DATABASE_URI"] = "sqlite:///chess.db"
app.config["SQLALCHEMY MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Game(db.Model):
    id = db.Column(db.String, primary_key=True)
    moves = db.Column(db.String, nullable=True)
    player1 = db.Column(db.String(20), nullable=False)
    player2 = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Game %r>' % self.id


def key_gen(s, n):
    key = []
    for i in range(n):
        key.append(s[randint(1, len(s) - 1)])
    return "".join(key)


@app.route('/')
def index():
    return render_template("main.html")


@app.route('/lobby')
def about():
    return render_template("lobby.html")


if __name__ == "__main__":
    app.run(debug=True)
