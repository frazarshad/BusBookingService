from flask import Flask, render_template, url_for, redirect, request, session, g
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bithu'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://lR28u35RXd:SUS2Z5R7kC@remotemysql.com/lR28u35RXd'
db = SQLAlchemy(app)

from models import User,Route

@app.route('/')
def home():
    if g.user:
        return redirect(url_for('book'))
    return render_template('signup.html')



@app.route('/book')
def book():
    if g.user:
        rt = []
        routes = Route.query.all()

        for route in routes:
            rt.append(route.route_path)

        return render_template('book.html', rt=rt)

    return redirect(url_for('login_post'))

@app.route('/bookie', methods=['Post', 'Get'])
def bookie():
    selectdata= request.form.get('route')
    print('hello')
    return redirect(url_for('current'))


@app.route('/current')
def current():
    if g.user:
        return render_template('current.html')

    return redirect(url_for('login_post'))


@app.route('/history')
def history():
    if g.user:
        return render_template('history.html')

    return redirect(url_for('login_post'))


@app.route('/book#')
def travel():
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('userName', None)
    g.user=None
    return redirect(url_for('home'))



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':

        username = request.form.get('username')
        if len(username) > 20:
            return render_template('signup.html', error='Username  must be less than 20 char')
        if username.isnumeric():
            return render_template('signup.html', error='Username  must contain alphabets also')
        password = request.form.get('password')
        if len(password) > 20:
            return render_template('signup.html', error='Password  must be less than 20 char')
        email = request.form.get('email')
        if len(email) > 20:
            return render_template('signup.html', error='email  must be less than 20 char')
        contact = request.form.get('phone')

        if len(contact)> 20 :
            return render_template('signup.html', error='contact no. must be less than 20 char')
        if not contact.isnumeric() and len(contact) != 0:
            return render_template('signup.html', error='contact no. must be an integer')
        if len(username) == 0 or len(password) == 0 or len(email) == 0 or len(contact) == 0:
            return render_template('signup.html', error='Fields can not be empty')
        user = User.query.filter_by(username=username).all()
        em=User.query.filter_by(email=email).all()

        if user :
            return render_template('signup.html', error="Username in use")
        if em :
            return render_template('signup.html', error="Email in use")

        entry = User(username=username, password=password, email=email, contact=contact)
        db.session.add(entry)
        db.session.commit()

    return render_template('signup.html')



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



@app.before_request
def before_request():
  g.user = None
  if 'userName' in session:
      g.user = session['userName']


if __name__ == '__main__':
    app.run()
