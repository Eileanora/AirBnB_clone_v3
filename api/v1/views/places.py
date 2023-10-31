#!/usr/bin/python3
""" API routes for User objects """

from flask import Flask, make_response, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.state import State
from models.user import User


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def places(city_id):
    """Retrieves the list of all Place objects of a City"""

    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    places_list = []
    for place in city.places:
        places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route('/places/<place_id>', strict_slashes=False)
def place(place_id):
    """Retrieves a Place object"""

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Deletes a Place object"""

    all_places = storage.all(Place)
    if "Place." + place_id not in all_places.keys():
        abort(404)

    place = all_places.get("Place." + place_id)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if not request.json:
        abort(400, "Not a JSON")

    if "user_id" not in request.json:
        abort(400, "Missing user_id")

    if "name" not in request.json:
        abort(400, "Missing name")

    user = storage.get(User, request.json.get("user_id"))
    if user is None:
        abort(404)

    place = request.get_json()
    new_place = Place(**place)
    new_place.city_id = city_id
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_places(place_id):
    """Updates a Place object"""

    if not request.json:
        abort(400, "Not a JSON")

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    for key, value in request.get_json().items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    place.save()
    return make_response(jsonify(place.to_dict()), 200)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """Search for places objects"""

    if not request.json:
        abort(400, "Not a JSON")

    results = []

    js = request.get_json()
    if js and len(js):
        states = request.json.get("states", None)
        cities = request.json.get("cities", None)
        amenities = request.json.get("amenities", None)

    if not js or not len(js) or not states and not cities and not amenities:
        for place in storage.all(Place).values():
            results.append(place.to_dict())
        return jsonify(results)

    if states:
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            results.append(place.to_dict())

    if cities:
        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                for place in city.places:
                    if place not in results:
                        results.append(place.to_dict())

    if amenities:
        old_results = results[:]
        results = []
        for place in old_results:
            place_amenities = []
            for amenity_id in place["amenities"]:
                place_amenities.append(amenity_id)
            if all(amenity in place_amenities
                   for amenity in request.json["amenities"]):
                results.append(place.to_dict())

    return jsonify(results)
