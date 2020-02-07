from datetime import datetime
from flask import request, jsonify, current_app
from app import db
from app.models import Aircrafts_data, Aircrafts_data_Schema
#Airports_data, Airports_data_Schema, \
#    Boarding_passes, Boarding_passes_Schema, Flights, Flights_Schema, \
#        Seats, Seats_Schema, Ticket_flights, Ticket_flights_Schema, Tickets, Tickets_Schema
from app.api import bp
from app.api.errors import response

#initializing ma.Schemas
Aircraft_data_s = Aircrafts_data_Schema()
Aircrafts_data_s = Aircrafts_data_Schema(many=True)
#Airport_data_s = Airports_data_Schema()
#Airports_data_s = Airports_data_Schema(many=True)
#Board_passes_s = Boarding_passes_Schema()
#Boarding_passes_s = Boarding_passes_Schema(many=True)
#Flight_s = Flights_Schema()
#Flights_s = Flights_Schema(many=True)
#Seat_s = Seats_Schema()
#Seats_s = Seats_Schema(many=True)
#Ticket_flight_s = Ticket_flights_Schema()
#Ticket_flights_s = Ticket_flights_Schema(many=True)
#Ticket_s = Tickets_Schema()
#Tickets_s = Tickets_Schema(many=True)

@bp.route('/aircrafts', methods=['GET'])
def get_aircrafts():
    all_aircrafts = Aircrafts_data.query.all()
    return jsonify(Aircrafts_data_s.dump(all_aircrafts))