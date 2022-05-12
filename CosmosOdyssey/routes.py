from flask import render_template, request, flash, url_for, redirect
from CosmosOdyssey import app
from CosmosOdyssey import database

planets = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]


@app.route("/")
def home():
    return redirect(url_for("flights"))


@app.route("/flights")
def flights():
    to_planet = request.args.get("To")
    from_planet = request.args.get("From")
    available_flights = []
    all_companies = database.getAllCompanies()
    if to_planet is None or from_planet is None:
        return render_template("flights.html", planets=planets, flights=available_flights, companies=all_companies)

    if to_planet not in planets or from_planet not in planets:
        flash("Please select correct planet(s)", "danger")
        return render_template("flights.html", planets=planets, flights=available_flights, companies=all_companies)
    if to_planet == from_planet:
        flash("Can't fly to the same planet", "warning")
        return render_template("flights.html", planets=planets, flights=available_flights, companies=all_companies)

    # Get all available routes based on search and order criteria
    companies_to_search = request.args.getlist("comp")
    available_flights = database.getAllFlights(from_planet=from_planet, to_planet=to_planet,
                                               sort_by=request.args.get("OrderBy"),
                                               companies_to_search=companies_to_search)

    if len(available_flights) == 0:
        flash("No flights found", "warning")
    else:
        flash("Found {} flights".format(len(available_flights)), "success")
    return render_template("flights.html", planets=planets, flights=available_flights, companies=all_companies)


@app.route("/reserve/<flight_id>", methods=["GET", "POST"])
def reserve_flight(flight_id):
    flight_info = database.getFlightFromID(flight_id)
    if flight_info is None:
        flash("Flight doesn't exist", "danger")
        return redirect(url_for("home"))
    if request.method == "GET":
        return render_template("reserve.html", flight_info=flight_info)

    if request.method == "POST":
        first_name = request.form["FirstName"].lower().strip()
        last_name = request.form["LastName"].lower().strip()
        if first_name is None or last_name is None or first_name == "" or last_name == "":
            flash("First and last name are required to reserve a flight ticket", "danger")
            return render_template("reserve.html", flight_info=flight_info)

        reserve_result_message, reserve_result_type = database.reserveTicket(flight_id=flight_id, first_name=first_name,
                                                                             last_name=last_name)
        flash(reserve_result_message, reserve_result_type)
        return render_template("reserve.html", flight_info=flight_info)


@app.route("/reservations")
def reservations():
    all_reservations = database.getReservations()
    return render_template("reservations.html", reservations=all_reservations)
