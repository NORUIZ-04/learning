from flask import Flask
from flask import jsonify
from flask import request
from flask_sqlalchemy import SQLAlchemy  # ORM

# ---------------------------------------------------------
# App initialization
# ---------------------------------------------------------
app = Flask(__name__)

# creating database
# Configure the database connection string.
# SQLite is used here — a lightweight, file-based database
# stored locally as "travel.db" in the project directory.
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///travel.db"

# Initialize the SQLAlchemy ORM instance and bind it to this Flask app.
# This 'db' object is used to define models and interact with the database.
db = SQLAlchemy(app)


# created the model for the database
# ---------------------------------------------------------
# Destination model
# Represents a single row in the "destination" table.
# Each attribute below maps directly to a column in the database.
# ---------------------------------------------------------
class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)              # unique identifier for each destination
    Destination = db.Column(db.String(50), nullable=False)    # name of the destination (required)
    country = db.Column(db.String(25), nullable=False)        # country the destination belongs to (required)
    rating = db.Column(db.Float, nullable=False)               # numeric rating score (required)

    # method inside the class to convert the row into dict format,
    # which helps us return clean JSON
    # Converts a Destination model instance into a plain Python dictionary.
    # This is necessary because Flask's jsonify() cannot serialize
    # SQLAlchemy model objects directly — only JSON-serializable types.
    def to_dict(self):
        return {
            "id": self.id,
            "destination": self.Destination,
            "country": self.country,
            "rating": self.rating
        }


# context manager - creates the tables if they don't exist yet
# Ensures the database schema (tables) is created before the app
# starts handling requests. app_context() is required because
# db.create_all() needs access to the current Flask app instance.
with app.app_context():
    db.create_all()


# create routes

# ---------------------------------------------------------
# Route: Home
# Purpose: Simple health-check / welcome endpoint to confirm
# the API is running.
# ---------------------------------------------------------
@app.route("/")  # the slash is used for the home route
def home():
    return jsonify({"message": "welcome to the travel api"})


# ---------------------------------------------------------
# Route: GET /destinations
# Purpose: Fetch and return ALL destinations from the database
# as a JSON array.
# ---------------------------------------------------------
@app.route("/destinations", methods=["GET"])
def get_destinations():
    destinations = Destination.query.all()
    return jsonify([destination.to_dict() for destination in destinations])



# ---------------------------------------------------------
# Route: GET /destinations/<id>
# Purpose: Fetch a SINGLE destination by its unique ID.
# Returns 404 with an error message if no matching record exists.
# ---------------------------------------------------------
@app.route("/destinations/<int:destination_id>", methods=["GET"])
def get_destination(destination_id):
    destination = Destination.query.get(destination_id)
    if destination:
        return jsonify(destination.to_dict())
    else:
        return jsonify({"error": "destination not found!"}), 404
#post request 


# ---------------------------------------------------------
# Route: POST /destinations
# Purpose: Create a NEW destination record from the JSON body
# sent in the request, save it to the database, and return
# the newly created record with a 201 (Created) status code.
# ---------------------------------------------------------
@app.route("/destinations", methods=["POST"])
def add_destination():
    data = request.get_json()
    destination = Destination(
        Destination=data["destination"],
        country=data["country"],
        rating=data["rating"]
    )
    db.session.add(destination)     # stage the new record for insertion
    db.session.commit()             # commit the transaction, saving it to the DB
    return jsonify(destination.to_dict()), 201


# ---------------------------------------------------------
# Entry point: run the Flask development server.
# debug=True enables auto-reload on code changes and detailed
# error pages — should be turned off in production.
# ---------------------------------------------------------
if __name__ == "__main__":  # keeps the api running with auto-reload on save
    app.run(debug=True)