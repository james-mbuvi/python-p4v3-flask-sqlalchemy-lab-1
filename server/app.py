# server/app.py

from flask import Flask, jsonify, make_response
from flask_migrate import Migrate
from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    return jsonify({'message': 'Flask SQLAlchemy Lab 1'})


@app.route('/earthquakes/<int:id>')
def earthquake_by_id(id):
    earthquake = Earthquake.query.get(id)
    if earthquake:
        return jsonify(earthquake.serialize()), 200
    else:
        return jsonify({'message': f'Earthquake {id} not found.'}), 404


@app.route('/earthquakes/magnitude/<float:magnitude>')
def earthquake_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    if earthquakes:
        return jsonify({
            'count': len(earthquakes),
            'quakes': [earthquake.serialize() for earthquake in earthquakes]
        }), 200
    else:
        return jsonify({'count': 0, 'quakes': []}), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)
