from app import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    contact = db.Column(db.Integer, unique=False, nullable=False)
    city = db.Column(db.String(20), unique=False, nullable=False)
    address = db.Column(db.String(50), unique=False, nullable=True)
    current_ride = db.Column(db.Integer, db.ForeignKey('running_rides`.id'), unique=False, nullable=False)


class Route(db.Model):
    __tablename__ = 'route'
    id = db.Column(db.Integer, primary_key=True)
    route_path = db.Column(db.String(50), nullable=False, unique=True)

class Bus(db.Model):
    __tablename__ = 'bus'
    id = db.Column(db.Integer, primary_key=True)
    capacity = db.Column(db.Integer, nullable=False)
    driver_name = db.Column(db.String(20), nullable=False)
    route = db.Column(db.Integer, db.ForeignKey('route.id'), nullable=False)

class RunningRides(db.Model):
    __tablename__ = 'running_rides'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, nullable=False)
    bus_number = db.Column(db.Integer, db.ForeignKey('bus.id'), nullable=False)

class Stop(db.Model):
    __tablename__ = 'stop'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    city = db.Column(db.String(20), unique=False, nullable=False)

class Invoice(db.Model):
    __tablename__ = 'invoice'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), unique=False, nullable=False)
    bus_number = db.Column(db.Integer, db.ForeignKey('bus.id'), unique=False, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    fare = db.Column(db.Float, nullable=False)