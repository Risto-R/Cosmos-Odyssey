import requests
from CosmosOdyssey import db
from CosmosOdyssey.models import Flights, Reservations
from dateutil.parser import parse
from datetime import datetime, timezone
import time
from CosmosOdyssey.Config import Config


def getFlightDataFromAPI():
    url = Config.API_URL
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    else:
        return None


def updateDatabase():
    """
    Gets data from API. Schedules next API check when current price list expires
    """
    db.create_all()

    data = getFlightDataFromAPI()
    if data is None:
        print("Failed to get data from API")
        print("Retrying in 60 seconds")
        time.sleep(60)
        updateDatabase()

    price_list_id = data["id"]
    valid_until = parse(data["validUntil"])

    # If price list exist then don't add to database
    all_price_list_ids = db.session.query(Flights.price_list_id).distinct().all()
    for elem in all_price_list_ids:
        if elem.price_list_id == price_list_id:
            # Schedule next API check
            time_until_next_api_call = valid_until - datetime.now(timezone.utc)
            print("Latest price is list already saved")
            print("Next api call at", valid_until)
            print("Time until next api call:", time_until_next_api_call.total_seconds(), "seconds")
            time.sleep(time_until_next_api_call.total_seconds())
            updateDatabase()
            return False

    legs = data["legs"]

    for elem in legs:
        leg_id = elem["id"]
        route_info = elem["routeInfo"]
        route_id = route_info["id"]
        route_from_id = route_info["from"]["id"]
        route_from_name = route_info["from"]["name"]
        route_to_id = route_info["to"]["id"]
        route_to_name = route_info["to"]["name"]
        route_distance = route_info["distance"]
        providers = elem["providers"]
        for provider in providers:
            provider_id = provider["id"]
            company_id = provider["company"]["id"]
            company_name = provider["company"]["name"]
            flight_start = parse(provider["flightStart"])
            flight_end = parse(provider["flightEnd"])
            flight_price = provider["price"]

            travel_time = round(abs(flight_end - flight_start).total_seconds() / 3600, 2)

            entry = Flights(price_list_id=price_list_id, valid_until=valid_until, leg_id=leg_id, route_id=route_id,
                            from_id=route_from_id,
                            from_name=route_from_name, to_id=route_to_id, to_name=route_to_name,
                            distance=route_distance, provider_id=provider_id, company_id=company_id,
                            company_name=company_name, price=flight_price, flight_start=flight_start,
                            flight_end=flight_end, travel_time=travel_time)
            db.session.add(entry)

    db.session.commit()

    # Schedule next API check
    time_until_next_api_call = valid_until - datetime.now(timezone.utc)
    print("New price list added to database")
    print("Next api call at", valid_until)
    print("Time until next api call:", time_until_next_api_call.total_seconds(), "seconds")
    databaseCleanup()
    time.sleep(time_until_next_api_call.total_seconds())
    updateDatabase()
    return True


def databaseCleanup():
    """
    Only allow flight table to have 15 price lists
    Delete flights in the earliest price list and also delete reservations for flights on that price list
    """
    all_price_lists = db.session.query(Flights.price_list_id).order_by(Flights.id.asc()).distinct(
        Flights.price_list_id).all()
    if len(all_price_lists) > 15:
        # Flights
        price_list_to_remove = all_price_lists[0].price_list_id
        db.session.query(Flights).filter(Flights.price_list_id == price_list_to_remove).delete()
        db.session.commit()
        # Reservations
        db.session.query(Reservations).filter(Reservations.price_list_id == price_list_to_remove).delete()
        db.session.commit()

    # print("PRICE LISTS IN DB:", "(", len(all_price_lists), ")", all_price_lists)
