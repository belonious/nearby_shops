import json

mimetype = 'application/json'
headers = {
    'Content-Type': mimetype,
    'Accept': mimetype
}


def test_error_radius(client):

    error_data = {
        "count": 5,
        "position": {"lat": 45.222, "lng": 333.33}
    }
    res = client.post('/search', data=json.dumps(error_data), headers=headers)
    assert res.status_code == 400
    assert res.json['error'] == "radius is required"


def test_error_count(client):

    error_data = {
        "radius": 543,
        "position": {"lat": 45.222, "lng": 333.33}
    }
    res = client.post('/search', data=json.dumps(error_data), headers=headers)
    assert res.status_code == 400
    assert res.json['error'] == "count is required"


def test_error_position(client):

    error_data = {
        "radius": 543,
        "count": 3
    }
    res = client.post('/search', data=json.dumps(error_data), headers=headers)
    assert res.status_code == 400
    assert res.json['error'] == "position is required"


def test_error_lat(client):

    error_data = {
        "radius": 543,
        "count": 3,
        "position": {"lng": 45.222}
    }
    res = client.post('/search', data=json.dumps(error_data), headers=headers)
    assert res.status_code == 400
    assert res.json['error'] == "position should have lat, lng"


def test_error_tags_type(client):

    error_data = {
        "radius": 543,
        "count": 3,
        "tags": "not valid type",
        "position": {"lng": 45.222, "lat": 45.33}
    }
    res = client.post('/search', data=json.dumps(error_data), headers=headers)
    assert res.status_code == 400
    assert res.json['error'] == "tags should be a list"


def test_return_structure(client):

    valid_data = {
        "radius": 200,
        "count": 5,
        "position": {"lng": 45.222, "lat": 45.33}
    }
    res = client.post('/search', data=json.dumps(valid_data), headers=headers)
    assert res.status_code == 200
    assert isinstance(res.json['products'], list)


def test_crash(client):

    error_data = {
        "radius": 200,
        "count": "OOOPPPPSSSS",
        "position": {"lng": 45.222, "lat": 45.33}
    }
    res = client.post('/search', data=json.dumps(error_data), headers=headers)
    assert res.status_code == 503
    assert res.json['error'] == 'service unavailable'


def test_tags(client):

    stockholm = {
        "radius": 2000,
        "count": 50,
        "tags": ["women"],
        "position": {"lng": 18.06, "lat": 59.33}
    }
    res = client.post('/search', data=json.dumps(stockholm), headers=headers)
    assert res.status_code == 200
    tags = set(map(lambda x: x.get('tag'), res.json['products']))
    assert len(tags) == 1