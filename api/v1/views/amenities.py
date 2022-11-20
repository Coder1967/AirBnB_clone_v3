#!/usr/bin/python3
"""Amenity objects that handles all default RESTFul API actions"""

from flask import request
from flask import abort
from flask import jsonify
from . import Amenity
from . import app_views
from . import storage


@app_views.route("/amenities", methods=["GET"])
def get_all_amenities():
    """ retrives all amenities stored """
    amenity_list = []

    for amenity in storage.all(Amenity).values():
        amenity_list.append(amenity.to_dict())
    return jsonify(amenity_list)


@app_views.route("/amenities/<amenity_id>", methods=["GET"])
def get_amenity(amenity_id):
    """ retrives a particular amenity instance using its id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    else:
        return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"])
def del_amenity(amenity_id):
    """  deletes a particular amenity using an id """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    else:
        storage.delete(amenity)
        storage.save()
        return jsonify({})


@app_views.route("/amenities", methods=["POST"])
def post_amenity():
    """ posts a amenity """
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    if req.get('name') is None:
        abort(400, 'Missing name')
    new_amenity = Amenity(**req)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"])
def put_amenity(amenity_id):
    """ updates an amenity"""
    amenity = storage.get(Amenity, amenity_id)
    req = request.get_json()
    restricted_attr = ['id', 'created_at', 'updated_at']

    if amenity is None:
        abort(404)
    if req is None:
        abort(400, "Not a JSON")
    for key in req.keys():
        if key not in restricted_attr:
            amenity.__dict__[key] = req[key]
    storage.save()
    return jsonify(amenity.to_dict())
