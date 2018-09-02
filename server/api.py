# -*- coding: utf-8 -*-

from flask import Blueprint, current_app, jsonify, request

from server.data import query_data

api = Blueprint('api', __name__)


def data_path(filename):
    data_path = current_app.config['DATA_PATH']
    return u"%s/%s" % (data_path, filename)


@api.route('/search', methods=['POST'])
def search():
    # validate post params todo add type validation
    data = request.get_json()
    if data.get('count') is None:
        return jsonify({'error': 'count is required'}), 400
    if data.get('radius') is None:
        return jsonify({'error': 'radius is required'}), 400
    if data.get('position') is None:
        return jsonify({'error': 'position is required'}), 400
    if data.get('position').get('lat') is None or data.get('position').get('lng') is None:
        return jsonify({'error': 'position should have lat, lng'}), 400
    if data.get('tags') and not isinstance(data.get('tags'), (list,)):
        return jsonify({'error': 'tags should be a list'}), 400

    # normalize values
    count = data.get('count')
    radius = data.get('radius') / 1000 # input is in meters
    lat = data.get('position').get('lat')
    lng = data.get('position').get('lng')
    tags = data.get('tags') or []
    try:
        products = query_data(count, lat, lng, radius, tags)
    except Exception as e:
        print e.message
        return jsonify({'error': 'service unavailable'}), 503
    return jsonify({
        'products': products.T.to_dict().values()
    })
