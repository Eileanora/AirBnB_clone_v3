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
