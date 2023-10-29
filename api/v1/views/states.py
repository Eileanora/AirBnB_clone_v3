#!/usr/bin/python3
""" Flask app """

from flask import Flask, make_response, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', defaults={"state_id": None}, strict_slashes=False)
@app_views.route('/states/<state_id>', strict_slashes=False)
def states(state_id):
    """ Retrieves the list of all State objects """
    all_states = storage.all("State")

    if state_id is not None:
        if "State." + state_id not in all_states.keys():
            abort(404)

        state = all_states.get("State." + state_id)
        return jsonify(state.to_dict())

    state_list = []

    for state in all_states.values():
        state_list.append(state.to_dict())

    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """ Deletes a State object """
    all_states = storage.all("State")
    if "State." + state_id not in all_states.keys():
        abort(404)

    state = all_states.get("State." + state_id)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ Creates a State object """
    if not request.json:
        abort(400, "Not a JSON")

    if "name" not in request.json:
        abort(400, "Missing name")

    state = request.get_json().get("name")
    new_state = State(name=state)
    storage.new(new_state)
    storage.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """ update a State object """
    if not request.json:
        abort(400, "Not a JSON")

    all_states = storage.all("State")
    if "State." + state_id not in all_states.keys():
        abort(404)

    state = all_states.get("State." + state_id)

    for key, value in request.get_json().items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)

    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
