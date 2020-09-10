#!/usr/bin/python3
""" Script to route the request """
from api.v1.views import app_views
from models.place import Place
from models import storage
from flask import jsonify, abort, request


@app_views.errorhandler(400)
def resource_bad_request(e):
    return jsonify({'error': str(e).replace('400 Bad Request: ', '')}), 400

@app_views.errorhandler(404)
def resource_not_found(e):
    return jsonify({'error': str(e).replace('404 Not FOund: ', '')}), 404

@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'], strict_slashes=False)
def get_places(city_id):
    """ Count the whole information in the database
        with the newly added count()"""
    if request.method == 'GET':
        dictionary = storage.all(Place)
        result = []
        for key, value in dictionary.items():
            if value.to_dict()['city_id'] == city_id: 
                result.append(value.to_dict())
        return jsonify(result), 201
    elif request.method == 'POST':
        print("entre al post")
        content = request.get_json(silent=True)
        if type(content) == dict:
            # is for valid if the pass is a json
            if 'name' not in content.keys():
                abort(400, "Missing name")
            if 'user_id' not in content.keys():
                abort(400, "Missing user_id")
            verify = storage.all(Place)
            checkcity = False
            checkuser = False
            for value in verify.values():
                if value.to_dict()['user_id'] == content['user_id']:
                    checkuser = True
                if value.to_dict()['city_id'] == content['city_id']:
                    checkcity = True
                if checkcity and checkuser:
                    break
            print(checkuser, checkcity)
            if not checkuser or not checkcity:
                abort(404, "not found ")
            dictionary = Place(**content)
            dictionary.save()
            # dictionary.save()
            return jsonify(dictionary.to_dict()), 201
        else:
            abort(400, "Not a JSON")
            # abort(400, description="fails cause yes")

@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def place_by_id(place_id):             
    """ get with id , delete the object and update the new object"""
    print(place_id)
    if request.method == 'GET':
        print("entre al get")
        result = storage.get(Place, place_id)
        if result:
            return jsonify(result.to_dict())
    elif request.method == 'DELETE':
        result = storage.get(Place, place_id)
        if result:
            result.delete()
            storage.save()
            return jsonify({})
    elif request.method == 'PUT':
        contents = request.get_json(silent=True)
        result = storage.get(Place, place_id)

        if not result:
            abort(404)
        if type(contents) == dict:
            dictionary = result.to_dict()
            for key, value in contents.items():
                if key not in ('id', 'user_id', 'city_id','created_at', 'updated_at'):
                    setattr(result, key, value)
            storage.save()
            return jsonify(result.to_dict()), 201
        else:
            abort(400, "Not a JSON")
            # abort(400, description="fails cause yes")
    abort(404)
