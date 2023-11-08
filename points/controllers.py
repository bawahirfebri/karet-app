from flask import request, jsonify, make_response
from .. import db
from . import models


def createPoint():
    try:
        data = request.get_json()
        newPoint = models.Point(
            longitude=data['longitude'], latitude=data['latitude'])
        db.session.add(newPoint)
        db.session.commit()
        return make_response(jsonify({'message': 'point created', 'data': newPoint.json()}), 201)
    except:
        return make_response(jsonify({'message': 'error creating point'}), 500)


def retrievePoints():
    try:
        points = models.Point.query.all()
        return make_response(jsonify([point.json() for point in points]), 200)
    except:
        return make_response(jsonify({'message': 'error retrieving points'}), 500)


def retrievePoint(id):
    try:
        point = models.Point.query.get(id)
        if point:
            return make_response(jsonify({'data': point.json()}), 200)
        return make_response(jsonify({'message': 'point not found with id={}'.format(id)}), 404)
    except:
        return make_response(jsonify({'message': 'error retrieving point'}), 500)


def updatePoint(id):
    try:
        point = models.Point.query.get(id)
        if point:
            data = request.get_json()
            point.longitude = data['longitude']
            point.latitude = data['latitude']
            db.session.commit()
            return make_response(jsonify({'message': 'point updated', 'data': point.json()}), 200)
        return make_response(jsonify({'message': 'point not found'}), 404)
    except:
        return make_response(jsonify({'message': 'error updating point'}))


def deletePoint(id):
    try:
        point = models.Point.query.get(id)
        if point:
            db.session.delete(point)
            db.session.commit()
            return make_response(jsonify({'message': 'point deleted'}), 200)
        return make_response(jsonify({'message': 'point not found'}), 404)
    except:
        return make_response(jsonify({'message': 'error deleting point'}), 500)
