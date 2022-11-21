#!/usr/bin/python3
"""User objects that handles all default RESTFul API actions"""

from flask import request
from flask import abort
from flask import jsonify
from . import User
from . import app_views
from . import storage


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_all_users():
    """ retrives all users stored """
    user_list = []

    for user in storage.all(User).values():
        user_list.append(user.to_dict())
    return jsonify(user_list)


@app_views.route("/users/<user_id>", methods=["GET"],
                 strict_slashes=False)
def get_user(user_id):
    """ retrives a particular user using an id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    else:
        return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
def del_user(user_id):
    """  deletes a particular user using an id """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    else:
        storage.delete(user)
        storage.save()
        return jsonify({})


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def post_user():
    """ adds a new user """
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    if 'email'not in req:
        abort(400, 'Missing email')
    if 'password' not in req:
        abort(400, 'Missing password')
    new_user = User(**req)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"],
                 strict_slashes=False)
def put_user(user_id):
    """ updates a user"""
    user = storage.get(User, user_id)
    req = request.get_json()
    restricted_attr = ['id', 'email', 'created_at', 'updated_at']

    if user is None:
        abort(404)
    if req is None:
        abort(400, "Not a JSON")
    for key in req.keys():
        if key not in restricted_attr:
            user.__dict__[key] = req[key]
    user.save()
    return jsonify(user.to_dict())
