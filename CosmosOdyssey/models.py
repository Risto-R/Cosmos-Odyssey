from CosmosOdyssey import db


class Flights(db.Model):
    __tablename__ = "flights"
    id = db.Column(db.Integer, primary_key=True)
    price_list_id = db.Column(db.String(100), nullable=False)
    valid_until = db.Column(db.DateTime, nullable=False)
    leg_id = db.Column(db.String(100), nullable=False)
    route_id = db.Column(db.String(100), nullable=False)
    from_id = db.Column(db.String(100), nullable=False)
    from_name = db.Column(db.String(100), nullable=False)
    to_id = db.Column(db.String(100), nullable=False)
    to_name = db.Column(db.String(100), nullable=False)
    distance = db.Column(db.Integer, nullable=False)
    provider_id = db.Column(db.String(100), nullable=False)
    company_id = db.Column(db.String(100), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    flight_start = db.Column(db.DateTime, nullable=False)
    flight_end = db.Column(db.DateTime, nullable=False)
    travel_time = db.Column(db.Float, nullable=False)


class Reservations(db.Model):
    __tablename__ = "reservations"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    total_price = db.Column(db.Integer, nullable=False)
    total_travel_time = db.Column(db.Integer, nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    provider_id = db.Column(db.String(100), db.ForeignKey("flights.provider_id"), nullable=False)
    price_list_id = db.Column(db.String(100), db.ForeignKey("flights.price_list_id"), nullable=False)
