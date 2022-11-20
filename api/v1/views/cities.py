#!/usr/bin/python3
"""City objects that handles all default RESTFul API actions"""

from flask import request
from flask import abort
from flask import jsonify
from . import State
from . import City
from . import app_views
from . import storage


@app_views.route("/states/<state_id>/cities", methods=["GET"])
def get_cities(state_id):
    """ retrives a list of cities of a state using the state's id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = []
    for city in state.cities:
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route('cities/<city_id>', methods=["GET"])
def get_city(city_id):
    """ retrives a city instance using its id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def del_city(city_id):
    """  deletes a particular city using its id """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        storage.delete(city)
        storage.save()
        return jsonify({})


@app_views.route("/states/<state_id>/cities", methods=["POST"])
def post_city(state_id):
    """ posts a city """
    req = request.get_json(state_id)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if req is None:
        abort(400, "Not a JSON")
    if req.get('name') is None:
        abort(400, 'Missing name')
    req['state_id'] = state_id
    new_city = City(**req)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"])
def put_city(city_id):
    """ updates a city"""
    city = storage.get(City, city_id)
    req = request.get_json()
    restricted_attr = ['id', 'state_id', 'created_at', 'updated_at']

    if city is None:
        abort(404)
    if req is None:
        abort(400, "Not a JSON")
    for key in req.keys():
        if key not in restricted_attr:
            city.__dict__[key] = req[key]
    storage.save()
    return jsonify(city.to_dict())
