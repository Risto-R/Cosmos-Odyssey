from CosmosOdyssey.models import Flights, Reservations
from CosmosOdyssey import db
from datetime import datetime


def getLatestPriceListID():
    return db.session.query(Flights).order_by(Flights.id.desc()).first().price_list_id


def getFlightFromID(provider_id):
    return db.session.query(Flights).filter(Flights.provider_id == provider_id).first()


def getReservations():
    s = db.session.query(Reservations).join(Flights, Reservations.provider_id == Flights.provider_id).add_columns(
        Flights.to_name, Flights.from_name).order_by(Reservations.id.desc()).all()
    return [row._asdict() for row in s]


def reserveTicket(flight_id, first_name, last_name):
    """
        Adds entry to RESERVATIONS table if flight is still valid and reservations
        Returns flash message and message type
    """
    flight_info = getFlightFromID(flight_id)
    # Make sure price list is still valid
    if flight_info.valid_until < datetime.utcnow():
        return "This ticket is no longer valid", "danger"

    if db.session.query(Reservations).filter(Reservations.first_name == first_name, Reservations.last_name == last_name,
                                             Reservations.provider_id == flight_id).first() is not None:
        return "You have already reserved this ticket", "warning"

    # Check if reservations exist

    entry = Reservations(first_name=first_name, last_name=last_name, total_price=flight_info.price,
                         total_travel_time=flight_info.travel_time, company_name=flight_info.company_name,
                         provider_id=flight_id, price_list_id=flight_info.price_list_id)
    db.session.add(entry)
    db.session.commit()
    return "Ticket has been reserved", "success"


def getAllFlights(from_planet, to_planet, sort_by, companies_to_search):
    latest_price_list_id = getLatestPriceListID()
    if len(companies_to_search) == 0:
        companies_to_search = getAllCompanies()
    if sort_by == "price_asc":
        available_flights = db.session.query(Flights).filter(Flights.to_name == to_planet,
                                                             Flights.from_name == from_planet,
                                                             Flights.price_list_id == latest_price_list_id,
                                                             Flights.company_name.in_(companies_to_search)).order_by(
            Flights.price.asc()).all()
    elif sort_by == "price_desc":
        available_flights = db.session.query(Flights).filter(Flights.to_name == to_planet,
                                                             Flights.from_name == from_planet,
                                                             Flights.price_list_id == latest_price_list_id,
                                                             Flights.company_name.in_(companies_to_search)).order_by(
            Flights.price.desc()).all()
    elif sort_by == "distance_asc":
        available_flights = db.session.query(Flights).filter(Flights.to_name == to_planet,
                                                             Flights.from_name == from_planet,
                                                             Flights.price_list_id == latest_price_list_id,
                                                             Flights.company_name.in_(companies_to_search)).order_by(
            Flights.distance.asc()).all()
    elif sort_by == "distance_desc":
        available_flights = db.session.query(Flights).filter(Flights.to_name == to_planet,
                                                             Flights.from_name == from_planet,
                                                             Flights.price_list_id == latest_price_list_id,
                                                             Flights.company_name.in_(companies_to_search)).order_by(
            Flights.distance.desc()).all()
    elif sort_by == "time_asc":
        available_flights = db.session.query(Flights).filter(Flights.to_name == to_planet,
                                                             Flights.from_name == from_planet,
                                                             Flights.price_list_id == latest_price_list_id,
                                                             Flights.company_name.in_(companies_to_search)).order_by(
            Flights.travel_time.asc()).all()
    elif sort_by == "time_desc":
        available_flights = db.session.query(Flights).filter(Flights.to_name == to_planet,
                                                             Flights.from_name == from_planet,
                                                             Flights.price_list_id == latest_price_list_id,
                                                             Flights.company_name.in_(companies_to_search)).order_by(
            Flights.travel_time.desc()).all()
    else:
        available_flights = db.session.query(Flights).filter(Flights.to_name == to_planet,
                                                             Flights.from_name == from_planet,
                                                             Flights.price_list_id == latest_price_list_id,
                                                             Flights.company_name.in_(companies_to_search)).order_by(
            Flights.price.asc()).all()

    return available_flights


def getAllCompanies():
    return [company[0] for company in db.session.query(Flights.company_name).distinct().all()]
