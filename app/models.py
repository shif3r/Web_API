from app import db, ma
from app.point import Point
from sqlalchemy.dialects.postgresql import CHAR, JSONB, INTEGER, TEXT, NUMERIC, TIMESTAMP, FLOAT

class Aircrafts_data(db.Model):
    __tablename__ = 'aircrafts_data'
    aircraft_code = db.Column(CHAR(3), primary_key=True)
    model = db.Column(JSONB, nullable=False)
    rrange = db.Column(INTEGER, nullable=False)

    def __init__(self, aircraft_code, model, rrange):
        self.aircraft_code = aircraft_code
        self.model = model
        self.rrange = rrange

class Airports_data(db.Model):
    __tablename__ = 'airports_data'
    airport_code = db.Column(CHAR(3), nullable=False, primary_key=True)
    airport_name = db.Column(JSONB, nullable=False)
    city = db.Column(JSONB, nullable=False)
    coordinates = db.Column(Point, nullable=False)
    timezone = db.Column(TEXT, nullable=False)

    def __init__(self, airport_code, airport_name, city, coordinates, timezone):
        self.airport_code = airport_code
        self.airport_name = airport_name
        self.city = city
        self.coordinates = coordinates
        self.timezone = timezone

class Boarding_passes(db.Model):
    __tablename__ = 'boarding_passes'
    __table_args__ = (
        db.UniqueConstraint('flight_id', 'boarding_no', name='boarding_passes_flight_id_boarding_no_key'),
        db.UniqueConstraint('flight_id', 'seat_no', name='boarding_passes_flight_id_seat_no_key'),
        db.PrimaryKeyConstraint('ticket_no', 'flight_id', name='boarding_passes_pkey'),
        db.ForeignKeyConstraint(['ticket_no', 'flight_id'],
            ['ticket_flights.ticket_no', 'ticket_flights.flight_id'], name='boarding_passes_ticket_no_fkey')
    )
    ticket_no = db.Column(CHAR(13), nullable=False)
    flight_id = db.Column(INTEGER, nullable=False)
    boarding_no = db.Column(INTEGER, nullable=False)
    seat_no = db.Column(CHAR(4), nullable=False)

    def __init__(self, ticket_no, flight_id, boarding_no, seat_no):
        self.ticket_no = ticket_no
        self.flight_id = flight_id
        self.boarding_no = boarding_no
        self.seat_no = seat_no

class Bookings(db.Model):
    __tablename__ = 'bookings'
    book_ref = db.Column(CHAR(6), nullable=False, primary_key=True)
    book_date = db.Column(TIMESTAMP, nullable=False)
    total_amount = db.Column(NUMERIC(scale=10, precision=2), nullable=False)

    def __init__(self, book_ref, book_date, total_amount):
        self.book_ref = book_ref
        self.book_date = book_date
        self.total_amount = total_amount

class Flights(db.Model):
    __tablename__ = 'flights'
    __table_args__ = (
        db.UniqueConstraint('flight_no', 'scheduled_departure', name='flights_flight_no_scheduled_departure_key'),
    )
    flight_id = db.Column(INTEGER, nullable=False, primary_key=True)
    flight_no = db.Column(CHAR(6), nullable=False)
    scheduled_departure = db.Column(TIMESTAMP, nullable=False)
    scheduled_arrival = db.Column(TIMESTAMP, nullable=False)
    departure_airport = db.Column(CHAR(3), db.ForeignKey('airports_data.airport_code'), nullable=False)
    arrival_airport = db.Column(CHAR(3), db.ForeignKey('airports_data.airport_code'), nullable=False)
    status = db.Column(CHAR(20), nullable=False)
    aircraft_code = db.Column(CHAR(3), db.ForeignKey('aircrafts_data.aircraft_code'), nullable=False)
    actual_departure = db.Column(TIMESTAMP, nullable=True)
    actual_arrival = db.Column(TIMESTAMP, nullable=True)

    def __init__(self, flight_id, flight_no, scheduled_departure, scheduled_arrival, departure_airport,
            arrival_airport, status, aircraft_code, actual_departure, actual_arrival):
        self.flight_id = flight_id
        self.flight_no = flight_no
        self.scheduled_departure = scheduled_departure
        self.scheduled_arrival = scheduled_arrival
        self.departure_airport = departure_airport
        self.arrival_airport = arrival_airport
        self.status = status
        self.aircraft_code = aircraft_code
        self.actual_departure = actual_departure
        self.actual_arrival = actual_arrival

class Seats(db.Model):
    __tablename__ = 'seats'
    __table_args__ = (db.PrimaryKeyConstraint('aircraft_code', 'seat_no', name='boarding_passes_pkey'),
        db.ForeignKeyConstraint(['aircraft_code'],
            ['aircrafts_data.aircraft_code'], name='boarding_passes_ticket_no_fkey'))
    aircraft_code = db.Column(CHAR(3), nullable=False)
    seat_no = db.Column(CHAR(4), nullable=False)
    fare_conditions = db.Column(CHAR(10), nullable=False)
    
    def __init__(self, aircraft_code, seat_no, fare_conditions):
        self.aircraft_code = aircraft_code
        self.seat_no = seat_no
        self.fare_conditions = fare_conditions

class Ticket_flights(db.Model):
    __tablename__ = 'ticket_flights'
    ticket_no = db.Column(CHAR(13), db.ForeignKey('tickets.ticket_no'), nullable=False, primary_key=True)
    flight_id = db.Column(INTEGER, db.ForeignKey('flights.flight_id'), nullable=False, primary_key=True)
    fare_conditions = db.Column(CHAR(10), nullable=False)
    amount = db.Column(NUMERIC(scale=10, precision=2), nullable=False)
        
    def __init__(self, ticket_no, flight_id, fare_conditions, amount):
        self.ticket_no = ticket_no
        self.flight_id = flight_id
        self.fare_conditions = fare_conditions
        self.amount = amount

class Tickets(db.Model):
    __tablename__ = 'tickets'
    ticket_no = db.Column(CHAR(13), nullable=False, primary_key=True)
    book_ref = db.Column(CHAR(6), db.ForeignKey('bookings.book_ref'), nullable=False)
    passenger_id = db.Column(CHAR(20), nullable=False)
    passenger_name = db.Column(TEXT, nullable=False)
    contact_data = db.Column(JSONB, nullable=True)
        
    def __init__(self, ticket_no, book_ref, passenger_id, passenger_name, contact_data):
        self.ticket_no = ticket_no
        self.book_ref = book_ref
        self.passenger_id = passenger_id
        self.passenger_name = passenger_name
        self.contact_data = contact_data

class Aircrafts_data_Schema(ma.ModelSchema):
  class Meta:
    fields = ('aircraft_code', 'model', 'rrange')

class Airports_data_Schema(ma.ModelSchema):
  class Meta:
    fields = ('airport_code', 'airport_name', 'city', 'coordinates', 'timezone')

class Boarding_passes_Schema(ma.ModelSchema):
  class Meta:
    fields = ('ticket_no', 'flight_id', 'boarding_no', 'seat_no')

class Bookings_Schema(ma.ModelSchema):
  class Meta:
    fields = ('book_ref', 'book_date', 'total_amount')

class Flights_Schema(ma.ModelSchema):
  class Meta:
    fields = ('flight_id', 'flight_no', 'scheduled_departure', 'scheduled_arrival', 'departure_airport',
        'arrival_airport', 'status', 'aircraft_code', 'actual_departure', 'actual_arrival')

class Seats_Schema(ma.ModelSchema):
  class Meta:
    fields = ('aircraft_code', 'seat_no', 'fare_conditions')

class Ticket_flights_Schema(ma.ModelSchema):
  class Meta:
    fields = ('ticket_no', 'flight_id', 'fare_conditions', 'amount')

class Tickets_Schema(ma.ModelSchema):
  class Meta:
    fields = ('ticket_no', 'book_ref', 'passenger_id', 'passenger_name', 'contact_data')