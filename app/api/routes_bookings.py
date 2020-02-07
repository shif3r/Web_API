from datetime import datetime
from flask import request, jsonify, current_app
from app import db
from app.models import Bookings, Bookings_Schema
#Aircrafts_data, Aircrafts_data_Schema, Airports_data, Airports_data_Schema, \
#    Boarding_passes, Boarding_passes_Schema, Flights, Flights_Schema, \
#        Seats, Seats_Schema, Ticket_flights, Ticket_flights_Schema, Tickets, Tickets_Schema
from app.api import bp
from app.api.errors import response, response_message

#initializing ma.Schemas
#Airport_data_s = Airports_data_Schema()
#Airports_data_s = Airports_data_Schema(many=True)
#Board_passes_s = Boarding_passes_Schema()
#Boarding_passes_s = Boarding_passes_Schema(many=True)
Booking_s = Bookings_Schema()
Bookings_s = Bookings_Schema(many=True)
#Flight_s = Flights_Schema()
#Flights_s = Flights_Schema(many=True)
#Seat_s = Seats_Schema()
#Seats_s = Seats_Schema(many=True)
#Ticket_flight_s = Ticket_flights_Schema()
#Ticket_flights_s = Ticket_flights_Schema(many=True)
#Ticket_s = Tickets_Schema()
#Tickets_s = Tickets_Schema(many=True)

@bp.route('/', methods=['GET', 'POST'])
def index():
    return jsonify({'msg': 'Hello World!'})

@bp.route('/bookings/<count>', methods=['GET'])
#Outputs last <count> of table 'Bookings'
def get_bookings(count):
    try:
        count = int(count)
    except:
        return response(400)
    if(count <= 0):
        response_message('Your number <= 0')
    all_bookings = Bookings.query.limit(count).all()
    return jsonify(Bookings_s.dump(all_bookings))

@bp.route('/bookings/book_ref/<book_ref>', methods=['GET'])
#Outputs <book_ref> of table 'Bookings'
def get_single_bookings(book_ref):
    try:
        int(book_ref)
        return response(400)
    except:
        pass
    booking = Bookings.query.get(book_ref)
    if not booking:
        return response(404)
    return jsonify(Booking_s.dump(booking))

@bp.route('/bookings', methods=['POST'])
#Adds a new booking into 'Bookings'
def add_booking():
    book_ref = request.json['book_ref']
    book_date = request.json['book_date']
    total_amount = request.json['total_amount']
    booking = Bookings(book_ref, book_date, total_amount)
    db.session.add(booking)
    db.session.commit()
    return Booking_s.jsonify(booking)

@bp.route('/bookings/book_ref/<book_ref>', methods=['DELETE'])
#Delete a row with <book_ref> pk from table 'Booking'
def delete_booking(book_ref):
    booking = Bookings.query.get(book_ref)
    if not booking:
        return response(404)
    db.session.delete(booking)
    db.session.commit()
    return Booking_s.jsonify(booking)

@bp.route('/bookings/book_ref/<book_ref>', methods=['PUT'])
#edits <book_ref> of table 'Bookings'
def update_booking(book_ref):
    booking = Bookings.query.get(book_ref)
    if not booking:
        return response(404)
    book_ref = request.json['book_ref']
    book_date = request.json['book_date']
    total_amount = request.json['total_amount']
    booking.book_ref = book_ref
    booking.book_date = book_date
    booking.total_amount = total_amount
    db.session.commit()
    return Booking_s.jsonify(booking)
