#!/usr/bin/python3
""" Script to route the request """
from api.v1.views import app_views
from models.user import User
from models import storage
from flask import jsonify, abort, request


@app_views.errorhandler(400)
def resource_not_found(e):
    return jsonify({'error': str(e).replace('400 Bad Request: ', '')}), 400

@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def get_users():
    """ Count the whole information in the database
        with the newly added count()"""

    if request.method == 'GET':
        dictionary = storage.all(User)
        result = []
        for clases in dictionary.values():
            result.append(clases.to_dict())
        return jsonify(result)

    if request.method == 'POST':
        content = request.get_json(silent=True)
        if not request.json:
            abort(400, "Not a JSON")

        if 'password' not in content.keys():
            abort(400, "Missing password")
        if 'email' not in content.keys():
            abort(400, "Missing email")

        dictionary = User(**content)
        dictionary.save()
        return jsonify(dictionary.to_dict()), 201


@app_views.route('/users/<string:user_id>', methods=['GET', 'PUT', 'DELETE'],
                 , strict_slashes=False)
def get_user_by_id(user_id):
    """ Extract the class of certain class delete
    the object and update the new object"""

    if request.method == 'GET':
        result = storage.get(User, user_id)
        if result:
            return jsonify(result.to_dict())
        else:
            abort(404)

    if request.method == 'DELETE':
        result = storage.get(User, user_id)
        if result:
            result.delete()
            storage.save()
            return jsonify({}), 200
        else:
            abort(404)

    if request.method == 'PUT':
        contents = request.get_json(silent=True)
        if not request.json:
            abort(400, "Not a JSON")

        result = storage.get(User, user_id)
        if not result:
            abort(404)

        for key, value in contents.items():
            if key not in ('id', 'created_at', 'updated_at'):
                setattr(result, key, value)
        storage.save()
        return jsonify(result.to_dict()), 200
