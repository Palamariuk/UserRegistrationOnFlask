from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    surname = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=True)
    age = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(128), nullable=False)
    gender = db.Column(db.String(32), nullable=False)

    def __init__(self, surname, name, email, age, city, gender):
        self.surname = surname
        self.name = name
        self.email = email
        self.age = age
        self.city = city
        self.gender = gender


genders = {"man": "Чоловік", "women": "Жінка", "other": "Інше"}

db.create_all()


@app.route('/')
def main_page():
    return render_template("register.html")


@app.route('/register', methods=["POST"])
def register():
    surname = request.form['surname']
    name = request.form['name']
    email = request.form['email']
    age = request.form['age']
    city = request.form['city']
    gender = genders[request.form['gender']]

    db.session.add(User(surname, name, email, age, city, gender))
    db.session.commit()
    return results()


@app.route('/results')
def results():
    users = User.query.all()
    return render_template("results.html", users=users)


if __name__ == '__main__':
    app.run()
