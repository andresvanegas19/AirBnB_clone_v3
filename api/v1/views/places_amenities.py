#!/usr/bin/python3
""" Script to give the and extract the information and
make endpoint """

from flask import jsonify, abort, request
from api.v1.views import app_views
from models.place import Place
from models.amenity import Amenity
from models import storage, storage_t
# storage_t is the variable that indicate which storage will use
from models.amenity import Amenity


# DBStorage: list, create and delete Amenity objects
# from amenities relationship


# FileStorage: list, add and remove Amenity ID in the
# list amenity_ids of a Place object

# GET /api/v1/places/<place_id>/amenities
@app_views.route('places/<string:place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def get_places(place_id):
    """  Is the function to retrive information of places related
    with Amenity, this function return a status and json """

    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if storage_t == "db":
        # with the relationship refer to amenaty to bring the peer
        return jsonify([amenity.to_dict() for amenity in place.amenities])
    else:
        return jsonify([amenity.to_dict() for amenity in place.amenities_list])


# DELETE /api/v1/places/<place_id>/amenities/<amenity_id>
# POST /api/v1/places/<place_id>/amenities/<amenity_id>
@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['DELETE', 'POST'], strict_slashes=False)
def update_amenity(place_id, amenity_id):
    """  Is the function to retrive information of specific places related
    with Amenity, this function return a status and json """

    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place or not amenity:
        abort(404)

    if request.method == 'DELETE':
        if storage_t == "db":
            # with the relationship refer to amenaty to bring the peer
            if amenity not in place.amenities:
                abort(404)
            amenity.delete()
            storage.save()
            return jsonify({})
        else:
            if 'place_id' in amenity.to_dict():
                if place_id == amenity.to_dict()['place_id']:
                    amenity.delete()
                    storage.save()
                    return jsonify({})
        abort(404)
