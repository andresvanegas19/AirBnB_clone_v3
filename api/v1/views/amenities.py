#!/usr/bin/python3
""" Script to give the and extrac the files """

# POST /api/v1/amenities
# GET /api/v1/amenities

# GET /api/v1/amenities/<amenity_id>
# DELETE /api/v1/amenities/<amenity_id>
# PUT /api/v1/amenities/<amenity_id>

from flask import jsonify, abort, request
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage


@app_views.errorhandler(400)
def resource_not_found(e):
    """ display an error of the """
    return jsonify(
        {
            'error': str(e).replace('400 Bad Request: ', '')
        }), 400


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def get_amenities():
    """ Count the whole information in the database
        of amenties and retrive this information"""

    # iterate throught the amenaties and become into dictionary and return it
    if request.method == 'GET':
        total = storage.all(Amenity)
        return jsonify([amenity.to_dict() for amenity in total.values()])
    if request.method == 'POST':
        content = request.get_json(silent=True)
        if not request.json:
            abort(400, "Not a JSON")
        if 'name' not in content.keys():
            abort(400, "Missing name")

        dictionary = Amenity(**content)
        dictionary.save()
        return jsonify(dictionary.to_dict()), 201


@app_views.route('amenities/<string:amenity_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def get_amenitie_by_id(amenity_id):
    """ Count the whole information in the database
        of amenties and retrive this information"""
    result = storage.get(Amenity, amenity_id)
    if not result:
        abort(404)

    if request.method == 'GET':
        return jsonify(result.to_dict())

    if request.method == 'DELETE':
        result.delete()
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")

        for key, value in request.get_json(silent=True).items():
            if key not in ('id', 'created_at', 'updated_at'):
                setattr(result, key, value)

        storage.save()
        return jsonify(result.to_dict()), 200
