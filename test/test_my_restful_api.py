import pytest
import os
import tempfile
import json
import requests

class TestMyRestfulApi():
    def test_user_get(self):
        name = 'Calvin' # already existing
        response = requests.get('http://127.0.0.1:5000/user/{}'.format(name))
        assert response.status_code == 200

        json_response = json.loads(response.text)
        assert json_response[0] == 'Calvin', "Expected response user name to be Calvin, instead was {}".format(json_response[0])
        assert json_response[1] == 24, "Expected response user age to be 24, instead was {}".format(json_response[1])
        assert json_response[2] == 'Software Engineer', "Expected response user occupation to be Software Engineer, instead was {}".format(json_response[2])

        # negative case 1: name not in db
        name_not_in_db = 'Helena'
        response = requests.get('http://127.0.0.1:5000/user/{}'.format(name_not_in_db))
        assert response.status_code == 404

        json_response = json.loads(response.text)
        assert json_response == 'User not found'

        # negative case 2: invalid name
        invalid_name = 83746
        response = requests.get('http://127.0.0.1:5000/user/{}'.format(invalid_name))
        assert response.status_code == 404

        json_response2 = json.loads(response.text)
        assert json_response2 == 'User not found'


    def test_user_post(self):
        name_to_insert = 'Steven'
        request = {"age": 40, "occupation": "Chef"}

        requests.delete('http://127.0.0.1:5000/user/{}'.format(name_to_insert), json=request)
        response = requests.post('http://127.0.0.1:5000/user/{}'.format(name_to_insert), json=request)
        assert response.status_code == 201

        json_response = json.loads(response.text)
        assert '{} was added.'.format(name_to_insert) == json_response

        response = requests.post('http://127.0.0.1:5000/user/{}'.format(name_to_insert), json=request)
        assert response.status_code == 400

        json_response = json.loads(response.text)
        assert "User with name {} already exists in db".format(name_to_insert) == json_response

    def test_user_put(self):
        name_to_insert = 'Stan'
        request = {"age": 32, "occupation": "Rapper"}

        requests.delete('http://127.0.0.1:5000/user/{}'.format(name_to_insert), json=request)
        response = requests.put('http://127.0.0.1:5000/user/{}'.format(name_to_insert), json=request)
        assert response.status_code == 201

        json_response = json.loads(response.text)
        assert "{} was added.".format(name_to_insert) == json_response

        new_request = {"age": 34, "occupation": "Music Producer"}
        response = requests.put('http://127.0.0.1:5000/user/{}'.format(name_to_insert), json=new_request)
        assert response.status_code == 200, "Expected status code 200, instead got {}".format(response.status_code)

        json_response = json.loads(response.text)
        assert "{} was updated.".format(name_to_insert) == json_response, "Expected user to be updated, instead received {}".format(json_response)

    def test_user_delete(self):
        user_to_delete = 'Haven'
        request = {"age": 21, "occupation": "Singer"}

        requests.put('http://127.0.0.1:5000/user/{}'.format(user_to_delete), json=request)
        response = requests.delete('http://127.0.0.1:5000/user/{}'.format(user_to_delete))

        assert response.status_code == 200
        assert "{} has been deleted.".format(user_to_delete) == json.loads(response.text)

        user_nonexistent = 'Winry'
        request = {"age": 24, "occupation": "Mechanic"}

        response = requests.delete('http://127.0.0.1:5000/user/{}'.format(user_nonexistent), json=request)
        assert response.status_code == 4043
        assert "User {} not in db".format(user_nonexistent) == json.loads(response.text)
