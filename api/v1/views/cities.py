#!/usr/bin/python3
""" Flask app """

from flask import Flask, make_response, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def cities(state_id):
    """ Retrieves the list of all City objects of a State """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    cities_list = []
    for city in state.cities:
        cities_list.append(city.to_dict())
    return make_response(jsonify(cities_list), 200)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def city(city_id):
    """ Retrieves a City object """
    city = storage.get(City, city_id)

    if city is None:
        abort(404)
    return make_response(jsonify(city.to_dict()), 200)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """ Deletes a City object """
    city = storage.get(City, city_id)
    if not city:
        return abort(404)

    city.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """ Creates a City object """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if not request.get_json:
        abort(400, "Not a JSON")

    if "name" not in request.get_json():
        abort(400, "Missing name")

    js_dict = request.get_json()
    new_city = City(**js_dict)
    new_city.state_id = state_id
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ update a City object """
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    if not request.get_json():
        abort(400, "Not a JSON")

    for key, value in request.get_json().items():
        if key not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
