from app import create_app, db
from app.models import Aircrafts_data, Airports_data, Boarding_passes, Bookings, Flights, Seats, \
    Ticket_flights, Tickets

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Aircrafts': Aircrafts_data, 'Airports': Airports_data,
            'Boarding_passes': Boarding_passes, 'Bookings': Bookings, 'Flights': Flights, 
            'Seats': Seats, 'Ticket_flights': Ticket_flights, 'Tickets': Tickets}