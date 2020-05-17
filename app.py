from flask import Flask, render_template, url_for, redirect, request, session, g
from flask_sqlalchemy import SQLAlchemy
import random
from datetime import date, time, datetime

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bithu'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://lR28u35RXd:SUS2Z5R7kC@remotemysql.com/lR28u35RXd'
db = SQLAlchemy(app)

from models import User, Route, Booking, Invoice

@app.route('/')
def home():
    if g.user:
        return redirect(url_for('book'))
    return render_template('signup.html')



@app.route('/book',methods=['POST','GET'])
def book():
    if g.user:
        if request.method == 'POST':
            rt = []
            routes = Route.query.all()
            for route in routes:
                rt.append(route.route_path)  # to display routes

            selectdata = request.form.get('route')  # get data from form
            selectdate = request.form.get('date')
            selecttime = request.form.get('time')
            if selectdate == "" or selecttime == "":
                return render_template('book.html', rt=rt, error='Date and Time cannot be left empty')

            ctime = date.today()
            convertdate= datetime.strptime(selectdate, '%Y-%m-%d').date()

            if convertdate< ctime:
                return render_template('book.html', rt=rt, error='Please select valid date')

            busstime = selectdate + " " + selecttime


            selectclass = request.form.get('class')
            entry = Booking(user=g.id, route=selectdata, date=busstime, bussClass=selectclass)
            db.session.add(entry)
            db.session.commit()

            return redirect(url_for('current'))

        rt = []
        routes = Route.query.all()
        for route in routes:
            rt.append(route.route_path)
        return render_template('book.html', rt=rt)

    return redirect(url_for('login_post'))


@app.route('/current')
def current():

    if g.user:
        checkTime()
        timelist=[]
        routedata = Booking.query.filter_by(user=g.id)
        ctime = datetime.now()
        ct= datetime.timestamp(ctime)
        for i in routedata:
            bt = datetime.timestamp(i.date)
            rt = bt-ct
            timelist.append(rt)

        return render_template('current.html', data=zip(routedata, timelist))

    return redirect(url_for('login_post'))

def checkTime():
    timelist = []
    routedata = Booking.query.filter_by(user=g.id)
    ctime = datetime.now()
    ct = datetime.timestamp(ctime)
    for i in routedata:
        bt = datetime.timestamp(i.date)
        rt = bt - ct
        timelist.append(rt)

    for data , rmt in zip(routedata, timelist):
        if rmt <= 0:
            entry = Invoice(user=data.user, date=data.date, fare=20, route=data.route, bussClass=data.bussClass)
            db.session.add(entry)
            Booking.query.filter_by(id=data.id).delete()
            db.session.commit()



@app.route('/cancel/<val>', methods=['GET','POST'])
def cancel(val):

    Booking.query.filter_by(id=val).delete()
    db.session.commit()
    return redirect(url_for('current'))

@app.route('/Clear', methods=['GET', 'POST'])
def Clear():
    Booking.query.filter_by(id=g.id).delete()
    db.session.commit()
    return render_template('history.html')

@app.route('/history')
def history():
    if g.user:
        data=Invoice.query.filter_by(user=g.id)
        return render_template('history.html', data=data)

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
        session['userId']=user.id
        session['userName'] = request.form['username']
        return redirect(url_for('book'))
    return render_template('signup.html')



@app.before_request
def before_request():


  g.user = None
  g.id = None
  if 'userName' in session:
      g.user = session['userName']
      g.id = session['userId']

if __name__ == '__main__':
    app.run()
