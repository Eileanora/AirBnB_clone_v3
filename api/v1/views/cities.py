#!/usr/bin/python3
""" Flask app """

from flask import Flask, make_response, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
import uuid


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def cities(state_id):
    """ Retrieves the list of all City objects of a State """
    state = storage.get(State, uuid.UUID(state_id))
    if state is None:
        abort(404)

    cities_list = []
    for city in state.cities:
        cities_list.append(city.to_dict())
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def city(city_id):
    """ Retrieves a City object """
    city = storage.get(City, uuid.UUID(city_id))

    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """ Deletes a City object """
    city = storage.get(City, uuid.UUID(city_id))

    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """ Creates a City object """
    state = storage.get(State, uuid.UUID(state_id))
    if state is None:
        abort(404)

    if not request.get_json:
        abort(400, "Not a JSON")

    if "name" not in request.get_json():
        abort(400, "Missing name")

    city = request.get_json().get("name")
    new_city = City(name=city, state_id=state_id)
    storage.new(new_city)
    storage.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ update a City object """
    city = storage.get(City, uuid.UUID(city_id))

    if city is None:
        abort(404)

    if not request.get_json:
        abort(400, "Not a JSON")

    for key, value in request.get_json().items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
