#!/usr/bin/python3
"""Place objects that handles all default RESTFul API actions"""

from flask import request
from flask import abort
from flask import jsonify
from . import Place
from . import State
from . import Amenity
from . import User
from . import City
from . import app_views
from flask import make_response
from . import storage


@app_views.route('/cities/<city_id>/places', methods=["GET"],
                 strict_slashes=False)
def get_places(city_id):
    """ gets all places in a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = []
    for place in city.places:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """ retrives a place instance using its id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id):
    """deletes an instance of place"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """adds new place"""
    req = request.get_json()
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if req is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in req:
        abort(400, 'Missing user_id')
    if 'name' not in req:
        abort(400, 'Missing name')
    user = storage.get(User, req['user_id'])
    if user is None:
        abort(404)
    req['city_id'] = city.id
    new_place = Place(**req)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """ updates a place object"""
    req = request.get_json()
    place = storage.get(Place, place_id)
    restricted = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

    if place is None:
        abort(404)
    if req is None:
        abort(400, 'Not a JSON')
    for key in req.keys():
        if key not in restricted:
            setattr(place, key, req[key])
    return jsonify(place.to_dict())
