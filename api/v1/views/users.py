#!/usr/bin/python3
""" API routes for User objects """

from flask import Flask, make_response, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', defaults={"user_id": None}, strict_slashes=False)
@app_views.route('/users/<user_id>', strict_slashes=False)
def users(user_id):
    """Retrieves the list of all User objects \
or a specific User object by id"""

    all_users = storage.all(User)

    if user_id is not None:
        if "User." + user_id not in all_users.keys():
            abort(404)

        user = all_users.get("User." + user_id)
        return jsonify(user.to_dict())

    user_list = []
    for user in all_users.values():
        user_list.append(user.to_dict())

    return jsonify(user_list)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """ Deletes a User object """

    all_users = storage.all(User)
    if "User." + user_id not in all_users.keys():
        abort(404)

    user = all_users.get("User." + user_id)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ Creates a User object """

    if not request.json:
        abort(400, "Not a JSON")

    if "email" not in request.json:
        abort(400, "Missing email")

    if "password" not in request.json:
        abort(400, "Missing password")

    user = request.get_json()
    new_user = User(**user)
    storage.new(new_user)
    storage.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """ update a User object """

    if not request.json:
        abort(400, "Not a JSON")

    all_users = storage.all(User)
    if "User." + user_id not in all_users.keys():
        abort(404)

    user = all_users.get("User." + user_id)
    user_dict = request.get_json()
    for key, value in user_dict.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
