from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Pokemon(db.Model):
    idx = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type1 = db.Column(db.String(100), nullable=False)
    type2 = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"{self.name}, {self.type1}, {self.type2}"


@app.route("/", methods=["GET"])
def index():
    pokemon = Pokemon.query.order_by(Pokemon.name).all()
    return render_template("index.html", pokemon=pokemon)


@app.route("/delete/<int:idx>", methods=["GET"])
def delete(idx):
    pokemon = Pokemon.query.get_or_404(idx)
    try:
        db.session.delete(pokemon)
        db.session.commit()
        return redirect(url_for("index"))
    except:
        return "Could not delete Pokemon"


@app.route("/create", methods=["POST"])
def create():
    name = request.form.get("name")
    type1 = request.form.get("type1")
    type2 = request.form.get("type2")
    p = Pokemon(name=name, type1=type1, type2=type2)
    try:
        db.session.add(p)
        db.session.commit()
        return redirect(url_for("index"))
    except:
        return "Can't add Pokemon"


@app.route("/update/<int:idx>", methods=["GET"])
def update_view(idx):
    pokemon = Pokemon.query.get_or_404(idx)
    return render_template("update.html", pokemon=pokemon)


@app.route("/update/<int:idx>", methods=["POST"])
def update(idx):
    pokemon = Pokemon.query.get_or_404(idx)
    pokemon.name = request.form.get("name")
    pokemon.type1 = request.form.get("type1")
    pokemon.type2 = request.form.get("type2")
    try:
        db.session.commit()
        return redirect(url_for("index"))
    except:
        return "Can't update Pokemon"


if __name__ == "__main__":
    db.create_all()
    app.run()
