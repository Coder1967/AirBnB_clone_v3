#!/usr/bin/python3
"""State objects that handles all default RESTFul API actions"""

from flask import request
from flask import abort
from flask import jsonify
from . import State
from . import app_views
from . import storage


@app_views.route("/states", methods=["GET", "post"])
def all_state():
    if request.method == 'GET':
        """ retrives all states stored """
        state_list = []

        for state in storage.all(State).values():
            state_list.append(state.to_dict())
        return jsonify(state_list)
    else:
        """ posts a state """
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    if req.get('name') is None:
        abort(400, 'Missing name')
    new_state = State(**req)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["GET", 'DELETE', 'PUT'])
def state(state_id):
    if request.method == 'GET':
        """ retrives a particular state using an id"""
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        else:
            return jsonify(state.to_dict())
    elif request.method == 'DELETE':
        """  deletes a particular state using an id """
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        else:
            storage.delete(state)
            storage.save()
            return jsonify({})
    else:
        """ updates a state"""
        state = storage.get(State, state_id)
        req = request.get_json()
        restricted_attr = ['id', 'created_at', 'updated_at']

        if state is None:
            abort(404)
        if req is None:
            abort(400, "Not a JSON")
        for key in req.keys():
            if key not in restricted_attr:
                state.__dict__[key] = req[key]
        state.save()
        return jsonify(state.to_dict())
