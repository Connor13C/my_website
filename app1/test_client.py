"""
This module contains an example of a requests based test for the example app.
Feel free to modify this file in any way.
"""
import requests
import uuid

# testing constants that match values in auth.py
BASE_URL = "http://127.0.0.1:5000"
ACCESS_TOKEN_1 = "31cd894de101a0e31ec4aa46503e59c8"
ACCESS_TOKEN_2 = "97778661dab9584190ecec11bf77593e"
USERNAME_1 = "challengeuser1"
USERNAME_2 = "challengeuser2"
USER_ID_1 = "8bde3e84-a964-479c-9c7b-4d7991717a1b"
USER_ID_2 = "45e3c49a-c699-405b-a8b2-f5407bb1a133"
headers_1 = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + ACCESS_TOKEN_1
}
headers_2 = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + ACCESS_TOKEN_2
}
headers_missing = {
            "Accept": "application/json",
            "Content-Type": "application/json"
}
headers_invalid = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + str(uuid.uuid4())
}
project_keys = ["project_id", "owner_id", "owner_username", "project_name", "comments"]
comment_keys = ["comment_id", "commenter_id", "commenter_username", "message"]


def make_project():
    path = BASE_URL + "/projects"
    body = {"project_name": "test project"}
    r = requests.post(path, headers=headers_1, json=body)
    assert r.status_code == 201
    resp = r.json()
    return resp["project_id"]


def delete_project(project_id):
    path = BASE_URL + f"/projects/{project_id}"
    r = requests.delete(path, headers=headers_1)
    assert r.status_code == 200


def test_example():
    """
    Example of using requests to make a test call to the example Flask app
    """
    path = BASE_URL + "/"
    r = requests.get(path, headers=headers_1)
    message = r.json()["message"]
    assert "Hello {}".format(USERNAME_1) in message
    r = requests.get(path, headers=headers_2)
    message = r.json()["message"]
    assert "Hello {}".format(USERNAME_2) in message


def test_projects_post():
    """
    Tests a post on /projects endpoint. Ensures status code is correct
    and json contains expected keys.
    """
    path = BASE_URL + "/projects"
    body = {"project_name": "test project"}
    r = requests.post(path, headers=headers_1, json=body)
    assert r.status_code == 201
    resp = r.json()
    assert all([True if key in project_keys else False for key in resp.keys()])
    delete_project(resp["project_id"])


def test_projects_post_missing_auth():
    """
    Tests a post request with missing authorization header on /projects endpoint.
    Ensures status code is correct.
    """
    path = BASE_URL + "/projects"
    body = {"project_name": "test project"}
    r = requests.post(path, headers=headers_missing, json=body)
    assert r.status_code == 401


def test_projects_post_invalid_auth():
    """
    Tests a post request with invalid bearer token on /projects endpoint.
    Ensures status code is correct.
    """
    path = BASE_URL + "/projects"
    body = {"project_name": "test project"}
    r = requests.post(path, headers=headers_invalid, json=body)
    assert r.status_code == 401


def test_projects_post_missing_name():
    """
    Tests a post request missing project_name in body on /projects endpoint.
    Ensures status code is correct.
    """
    path = BASE_URL + "/projects"
    body = {}
    r = requests.post(path, headers=headers_1, json=body)
    assert r.status_code == 400


def test_projects_get():
    """
    Tests a get request on /projects endpoint with no get resource.
    Ensures status code is correct.
    """
    path = BASE_URL + "/projects"
    r = requests.get(path, headers=headers_1)
    assert r.status_code == 405


def test_project_get():
    """
    Tests a get request on /projects/<project_id>.
    Ensures status code is correct and json had expected keys.
    """
    project_id = make_project()
    path = BASE_URL + f"/projects/{project_id}"
    r = requests.get(path, headers=headers_1)
    assert r.status_code == 200
    resp = r.json()
    assert all([True if key in project_keys else False for key in resp.keys()])
    delete_project(project_id)


def test_project_get_invalid_id():
    """
    Tests a get request on /projects/<project_id> with invalid project_id.
    Ensures status code is correct.
    """
    path = BASE_URL + f"/projects/{str(uuid.uuid4())}"
    r = requests.get(path, headers=headers_1)
    assert r.status_code == 404


def test_project_get_missing_auth():
    """
    Tests a get request with missing authorization header on /projects/<project_id>.
    Ensures status code is correct.
    """
    project_id = make_project()
    path = BASE_URL + f"/projects/{project_id}"
    r = requests.get(path, headers=headers_missing)
    assert r.status_code == 401
    delete_project(project_id)


def test_project_get_invalid_auth():
    """
    Tests a get request with invalid bearer token on /projects/<project_id>.
    Ensures status code is correct.
    """
    project_id = make_project()
    path = BASE_URL + f"/projects/{project_id}"
    r = requests.get(path, headers=headers_invalid)
    assert r.status_code == 401
    delete_project(project_id)


def test_project_delete():
    """
    Tests delete request on /projects/<project_id>.
    Ensures status code is correct and json contains expected keys.
    """
    project_id = make_project()
    path = BASE_URL + f"/projects/{project_id}"
    r = requests.delete(path, headers=headers_1)
    assert r.status_code == 200
    resp = r.json()
    assert all([True if key in project_keys else False for key in resp.keys()])


def test_project_delete_missing_auth():
    """
    Tests a delete request with miss authorization header on /projects/<project_id>.
    Ensures status code is correct.
    """
    project_id = make_project()
    path = BASE_URL + f"/projects/{project_id}"
    r = requests.delete(path, headers=headers_missing)
    assert r.status_code == 401
    delete_project(project_id)


def test_project_delete_invalid_auth():
    """
    Tests a get request with invalid bearer token on /projects/<project_id>.
    Ensures status code is correct.
    """
    project_id = make_project()
    path = BASE_URL + f"/projects/{project_id}"
    r = requests.delete(path, headers=headers_invalid)
    assert r.status_code == 401
    delete_project(project_id)


def test_project_delete_invalid_id():
    """
    Tests a get request with invalid project id on /projects/<project_id>.
    Ensures status code is correct.
    """
    path = BASE_URL + f"/projects/{str(uuid.uuid4())}"
    r = requests.delete(path, headers=headers_1)
    assert r.status_code == 404


def test_comments_post():
    """
    Tests a post request on /projects/<project_id>/comments.
    Ensures status code is correct and json contains expected keys.
    """
    project_id = make_project()
    path = BASE_URL + f"/projects/{project_id}/comments"
    body = {"message": "test comment"}
    r = requests.post(path, headers=headers_1, json=body)
    assert r.status_code == 201
    resp = r.json()
    assert all([True if key in comment_keys else False for key in resp.keys()])
    delete_project(project_id)


def test_comments_post_missing_auth():
    """
    Tests a post request with missing authentication header on
    /projects/<project_id>/comments.
    Ensures status code is correct.
    """
    project_id = make_project()
    path = BASE_URL + f"/projects/{project_id}/comments"
    body = {"message": "test comment"}
    r = requests.post(path, headers=headers_missing, json=body)
    assert r.status_code == 401
    delete_project(project_id)


def test_comments_post_invalid_auth():
    """
    Tests a post request with invalid bearer token on /projects/<project_id>/comments.
    Ensures status code is correct.
    """
    project_id = make_project()
    path = BASE_URL + f"/projects/{project_id}/comments"
    body = {"message": "test comment"}
    r = requests.post(path, headers=headers_invalid, json=body)
    assert r.status_code == 401
    delete_project(project_id)


def test_comment_post_invalid_project_id():
    """
    Tests a post request with invalid project_id on /projects/<project_id>/comments.
    Ensures status code is correct.
    """
    path = BASE_URL + f"/projects/{str(uuid.uuid4())}/comments"
    body = {"message": "test comment"}
    r = requests.post(path, headers=headers_1, json=body)
    assert r.status_code == 404


def test_comment_post_missing_message():
    """
    Tests a get request with missing message in body on /projects/<project_id>/comments.
    Ensures status code is correct.
    """
    project_id = make_project()
    path = BASE_URL + f"/projects/{project_id}/comments"
    body = {}
    r = requests.post(path, headers=headers_1, json=body)
    assert r.status_code == 400
    delete_project(project_id)


if __name__ == "__main__":
    test_example()
