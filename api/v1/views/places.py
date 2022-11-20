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

@app_views.route('/cities/<city_id>/places', methods=["GET"])
def get_places(city_id):
    """ gets all places in a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = []
    all_places = storage.all(Place)
    for place in all_places.values():
        if place.city_id == city.id:
            places.append(place.to_dict())
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """ retrives a place instance using its id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def del_place(place_id):
    """deletes an instance of place"""
    place = storage.get(Place, place_id)
    
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def post_place(city_id):
    """adds new place"""
    req = request.get_json()
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if req is None:
        abort(400, 'Not a JSON')
    if req.get('name') is None:
        abort(400, 'Missing user_id')
    req['city_id'] = city.id
    new_place = Place(**req)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def post_search():
    """searches for a particular place"""
    if request.get_json() is not None:
        req = request.get_json()
        states = req.get('states', [])
        cities = req.get('cities', [])
        amenities = req.get('amenities', [])
        amenity_objects = []
        for amenity_id in amenities:
            amenity = storage.get(Amenity, amenity_id)
            if amenity:
                amenity_objects.append(amenity)
        if states == cities == []:
            places = storage.all(Place).values()
        else:
            places = []
            for state_id in states:
                state = storage.get(State, state_id)
                state_cities = state.cities
                for city in state_cities:
                    if city.id not in cities:
                        cities.append(city.id)
            for city_id in cities:
                city = storage.get(City, city_id)
                for place in city.places:
                    places.append(place)
        confirmed_places = []
        for place in places:
            place_amenities = place.amenities
            confirmed_places.append(place.to_dict())
            for amenity in amenity_objects:
                if amenity not in place_amenities:
                    confirmed_places.pop()
                    break
        return jsonify(confirmed_places)
    else:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
