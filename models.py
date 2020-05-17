from app import db, render_template

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    contact = db.Column(db.Integer, unique=False, nullable=False)
    city = db.Column(db.String(20), unique=False, nullable=False, default='Lahore')
    address = db.Column(db.String(50), unique=False, nullable=True)
    current_ride = db.Column(db.Integer, db.ForeignKey('running_rides.id'), unique=False, nullable=True)



class Route(db.Model):
    __tablename__ = 'route'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    route_path = db.Column(db.String(50), nullable=False, unique=True)
    route_class = db.Column(db.String(30), nullable=False)



class Invoice(db.Model):
    __tablename__ = 'invoice'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), unique=False, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    fare = db.Column(db.Float, nullable=False)
    route = db.Column(db.String(50), nullable=False)
    bussClass = db.Column(db.String(30), nullable=False)

class Booking(db.Model):
    __tablename__ = 'booking'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), unique=False, nullable=False)
    route = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime,nullable=False)
    bussClass = db.Column(db.String(30), nullable=False)

