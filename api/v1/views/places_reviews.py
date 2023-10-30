#!/usr/bin/python3
""" API routes for review objects """

from flask import Flask, make_response, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def place_reviews(place_id):
    """Retrieves the list of all Review objects of a Place"""

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    reviews_list = []
    for review in place.reviews:
        reviews_list.append(review.to_dict())
    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def review(review_id):
    """Retrieves a Review object"""

    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Deletes a Review object"""

    all_reviews = storage.all(Review)
    if "Review." + review_id not in all_reviews.keys():
        abort(404)

    review = all_reviews.get("Review." + review_id)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Create a Review object"""

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if not request.json:
        abort(400, "Not a JSON")

    if "user_id" not in request.json:
        abort(400, "Missing user_id")

    user = storage.get(User, request.json.get("user_id"))
    if user is None:
        abort(404)

    if "text" not in request.json:
        abort(400, "Missing text")

    review = request.get_json()
    new_review = Review(**review)
    new_review.place_id = place_id
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """Update a Review object"""

    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    if not request.json:
        abort(400, "Not a JSON")

    for key, value in request.get_json().items():
        if key not in ["id", "user_id", "place_id",
                       "created_at", "updated_at"]:
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
