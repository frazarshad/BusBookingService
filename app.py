from flask import Flask, render_template, url_for, redirect, request, session, g
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bithu'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://lR28u35RXd:SUS2Z5R7kC@remotemysql.com/lR28u35RXd'
db = SQLAlchemy(app)

from models import User

@app.route('/')
def home():
    if g.user:
        return redirect(url_for('book'))
    return render_template('signup.html')



@app.route('/book.html')
def book():
    if g.user:
        return render_template('book.html')

    return redirect(url_for('login_post'))


@app.route('/current.html')
def current():
    if g.user:
        return render_template('current.html')

    return redirect(url_for('login_post'))


@app.route('/history.html')
def history():
    if g.user:
        return render_template('history.html')

    return redirect(url_for('login_post'))


@app.route('/book#')
def travel():
    return render_template('signup.html')

@app.route('/logout.html')
def logout():
    session.pop('userName', None)
    g.user=None
    return redirect(url_for('home'))



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

@app.before_request
def before_request():
  g.user = None
  if 'userName' in session:
      g.user = session['userName']


@app.route('/login', methods=['GET', 'POST'])
def login_post():


    if request.method == 'POST':
        session.pop('userName', None)

        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username, password=password).first()

        if not user or user.password != password:
            return render_template('signup.html', error="Username or password incorrect")
        session['userName'] = request.form['username']
        return redirect(url_for('book'))
    return render_template('signup.html')




if __name__ == '__main__':
    app.run()
