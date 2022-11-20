#!/usr/bin/python3
"""Place objects that handles all default RESTFul API actions"""

from flask import request
from flask import abort
from flask import jsonify
from . import Place
from . import User
from . import City
from . import app_views
from . import storage


@app_views.route("/cities/<city_id>/places", methods=["GET"])
def get_places(city_id):
    """ retrives a list of places of a city using the city's id"""
    all_place = storage.all(Place)
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = []
    for place in all_place.values():
        if (places.city_id == city_id):
            places.append(place.to_dict())
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=["GET"])
def get_place(place_id):
    """ retrives a place instance using its id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"])
def del_place(place_id):
    """  deletes a particular place using its id """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        storage.delete(place)
        storage.save()
        return jsonify({})


@app_views.route("/cities/<city_id>/places", methods=["POST"])
def post_place(city_id):
    """ adds a place """
    req = request.get_json()
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if req is None:
        abort(400, "Not a JSON")
    if req.get('name') is None:
        abort(400, 'Missing name')
    if req.get('user_id') is None:
        abort(400, 'Missing user_id')
    req['city_id'] = city_id
    new_place = Place(**req)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"])
def put_place(place_id):
    """ updates a place"""
    place = storage.get(Place, place_id)
    req = request.get_json()
    restricted_attr = ['id', 'city_id', 'user_id', 'created_at', 'updated_at']

    if place is None:
        abort(404)
    if req is None:
        abort(400, "Not a JSON")
    for key in req.keys():
        if key not in restricted_attr:
            place.__dict__[key] = req[key]
    storage.save()
    return jsonify(place.to_dict())
