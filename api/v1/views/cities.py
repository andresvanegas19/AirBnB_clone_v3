#!/usr/bin/python3
""" Script to give the and extrac the files """

from flask import jsonify, abort, request
from api.v1.views import app_views
from models.city import City
from models.state import State
from models import storage


@app_views.errorhandler(400)
def resource_not_found(e):
    """ display an error of the """
    return jsonify(
        {
            'error': str(e).replace('400 Bad Request: ', '')
        }), 400


# State: GET /api/v1/states/<state_id>/cities
# POST /api/v1/states/<state_id>/cities

# GET /api/v1/cities/<city_id>
# DELETE /api/v1/cities/<city_id>
# PUT /api/v1/cities/<city_id>


@app_views.route('/states/<string:state_id>/cities', methods=['POST', 'GET'],
                 strict_slashes=False)
def get_cities_by_state(state_id):
    """ Count the whole information in the database
        with the newly added count()"""

    if request.method == 'GET':
        for clases in storage.all(State).values():
            if state_id == clases.id:
                result = [city.to_dict() for city in clases.cities]
                return jsonify(result)
        abort(404)

    elif request.method == 'POST':
        content = request.get_json(silent=True)
        result = storage.get(State, state_id)
        if not result:
            abort(404)

        if type(content) == dict:
            if 'name' not in content.keys():
                abort(400, "Missing name")
            content['state_id'] = state_id
            dictionary = City(**content)
            dictionary.save()
            return jsonify(dictionary.to_dict()), 201
        else:
            abort(400, "Not a JSON")


@app_views.route('/cities/<string:city_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def get_cities(city_id):
    """ Count the whole information in the database
        with the newly added count()"""
    result = storage.get(City, city_id)
    if not result:
        abort(404)

    if request.method == 'GET':
        return jsonify(result.to_dict())

    if request.method == 'DELETE':
        if result:
            result.delete()
            storage.save()
            return jsonify({})

    if request.method == 'PUT':
        contents = request.get_json(silent=True)
        if not request.json:
            abort(400, "Not a JSON")

        for key, value in contents.items():
            if key not in ('id', 'created_at', 'updated_at'):
                setattr(result, key, value)

        storage.save()
        return jsonify(result.to_dict()), 200
