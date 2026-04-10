# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route("/earthquakes/<int:id>", methods=["GET"])
def get_single_earthquake(id):
    s_earthquake = Earthquake.query.filter_by(id=id).first()
    if s_earthquake:
        response={
            "id": s_earthquake.id,
            "location": s_earthquake.location,
            "magnitude": s_earthquake.magnitude,
            "year": s_earthquake.year
        }
        status = 200
    else:
        response = {"message": f"Earthquake {id} not found."}
        status = 404
        
    return make_response(response, status)
@app.route("/earthquakes/magnitude/<float:magnitude>")
def get_by_magnitude(magnitude):
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    quake_list = []
    for quake in quakes:
        quake_data={
            "id": quake.id,
            "location": quake.location,
            "magnitude": quake.magnitude,
            "year": quake.year
        }
        quake_list.append(quake_data)
    response = {'count': len(quake_list),
            'quakes': quake_list
            }
    return make_response(response, 200)
    


if __name__ == '__main__':
    app.run(port=5555, debug=True)
