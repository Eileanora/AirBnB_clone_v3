#!/usr/bin/python3
""" Amenities view that handles all RESTFUL API actions """

from flask import Flask, make_response, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', defaults={"amenity_id": None},
                 strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def amenties(amenity_id):
    """Retrives list of all amenities objects or \
a specific amenity object if id is given"""
    all_amenities = storage.all(Amenity)

    if amenity_id is not None:
        if "Amenity." + amenity_id not in all_amenities.keys():
            abort(404)
        amenity = all_amenities.get("Amenity." + amenity_id)
        return jsonify(amenity.to_dict())
    else:
        amenties_list = []
        for amenity in all_amenities.values():
            amenties_list.append(amenity.to_dict())
        return jsonify(amenties_list)

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Delete a specific amenity object"""
    all_amenties = storage.all(Amenity)
    if "Amenity." + amenity_id not in all_amenties.keys():
        abort(404)

    amenity = all_amenties.get("Amenity." + amenity_id)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Create a new amenity object"""
    if not request.json:
        abort(400, "Not a JSON")

    if "name" not in request.json:
        abort(400, "Missing name")

    amenity = request.get_json().get("name")
    new_amenity = Amenity(name=amenity)
    storage.new(new_amenity)
    storage.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """Update a specific amenity object"""
    all_amenities = storage.all(Amenity)
    if "Amenity." + amenity_id not in all_amenities.keys():
        abort(404)

    if not request.json:
        abort(400, "Not a JSON")

    amenity = all_amenities.get("Amenity." + amenity_id)
    amenity.name = request.get_json().get("name")
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
