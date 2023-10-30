#!/usr/bin/python3
""" Amenities view that handles all RESTFUL API actions """

from flask import Flask, make_response, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', defaults={"amenities_id": None}, strict_slashes=False)
def amenties():
    """Retrives list of all amenities objects"""
    amenities_list = []
    all_amenities = storage.all(Amenities)

@app_views.route('/amenities/<amenities_id>', strict_slashes=False)
def amenities(amenities_id):
