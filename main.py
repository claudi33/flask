import enum
from sqlalchemy import Enum
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
import os
import httpx

app = Flask('Bimba')

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

admin = Admin(app, name='MyAdmin', template_mode='bootstrap3')


class Gender(enum.Enum):
    male = 1
    female = 2


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    sex = db.Column(Enum(Gender), nullable=True)


admin.add_view(ModelView(User, db.session))

with app.app_context():
    db.create_all()


@app.route('/', methods=["POST", "GET"])
def home():
    name = None
    already_exists = False
    with open('user.txt', 'a') as file:
        if request.method == "POST":
            name = request.form['name'].strip().lower()
            existing_user = User.query.filter_by(name=name).first()
            if existing_user:
                already_exists = True
            else:
                new_user = User(name=name)
                db.session.add(new_user)
                db.session.commit()
                file.write("\nUser " + name.capitalize() + " created successfully")
        users = User.query.all()
        user_names = [user.name for user in users]
        return render_template('index.html', name=name, users=users, user_names=user_names,
                               already_exists=already_exists)


@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)


@app.route('/mems', methods=["POST", "GET"])
def mems():
    jokes = []
    num = 0
    if request.method == "POST":
        num = int(request.form.get('count', 0))
    for _ in range(num):
        res = httpx.get('https://v2.jokeapi.dev/joke/Programming')
        if res.status_code == 200:
            res1 = res.json()
            if not 'joke' in res1:
                jokes.append(f"{res1['setup']} - {res1['delivery']}")
            else:
                jokes.append(res1['joke'])
    return render_template('mems.html', jokes=jokes)


@app.route('/weather', methods=["POST", "GET"])
def weather():
    api_key = '8176cc6725d74095928150351252707'
    res1 = None
    city = None
    if request.method == "POST":
        city = request.form.get('city')
        base_url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}'
        res = httpx.get(base_url)
        if res.status_code == 200:
            res1 = res.json()
    return render_template('weather.html', res1=res1, city=city)


if __name__ == '__main__':
    app.run(debug=True)
