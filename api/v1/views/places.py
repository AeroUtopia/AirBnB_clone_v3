#!/usr/bin/python3
"""
    Handles API functions for Place
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def city_places(city_id):
    """
        Handles places in a specified city
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        place_list = []
        for place in city.places:
            place_list.append(place.to_dict())
        return jsonify(place_list)
    if request.method == 'POST':
        info = request.get_json(silent=True)
        if not info:
            abort(400, 'Not a JSON')
        if 'user_id' not in info:
            abort(400, 'Missing user_id')
        user = storage.get(User, info['user_id'])
        if user is None:
            abort(404)
        if 'name' not in info:
            abort(400, 'Missing name')
        info['city_id'] = city_id
        new_place = Place(**info)
        new_place.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def place_object(place_id):
    """
    Handles a specified Place
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(place.to_dict())
    if request.method == 'DELETE':
        for review in place.reviews:
            storage.delete(review)
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        info = request.get_json(silent=True)
        if not info:
            abort(400, 'Not a JSON')
        for key, value in info.items():
            if key in ['id', 'created_at', 'updated_at', 'user_id', 'city_id']:
                pass
            else:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200
