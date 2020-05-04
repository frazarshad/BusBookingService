from flask import Flask, render_template, url_for, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bithu'
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://lR28u35RXd:SUS2Z5R7kC@remotemysql.com/lR28u35RXd'
db = SQLAlchemy(app)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    contact = db.Column(db.Integer, unique=False, nullable=False)



@app.route('/')
def home():
    return render_template('signup.html')


@app.route('/book.html')
def book():
    return render_template('book.html')

@app.route('/current.html')
def current():
    return render_template('current.html')

@app.route('/history.html')
def history():
    return render_template('history.html')

@app.route('/book#')
def travel():
    return render_template('signup.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        contact = request.form.get('phone')

        user = User.query.filter_by(username=username).all()

        if user:
            return render_template('signup.html', error="Username in use")

        entry = User(username=username, password=password, email=email, contact=contact)
        db.session.add(entry)
        db.session.commit()

    return render_template('signup.html')


@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    if not user:
        flash('Incorrect user or password')
        return redirect(url_for('signup'))

    return redirect(url_for('book'))

if __name__ == '__main__':
    app.run()
