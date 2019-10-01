import pytest

from app import app


@pytest.fixture
def test_client():
    return app.test_client()


def test_index_get_ok(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Little bit of skills for the Flyps" in response.data
    assert b"Fibonacci" in response.data
    assert b"This is palindrome:" not in response.data


def test_fibonacci_calc_post_ok(test_client):
    payload = {
        'fibonacci': 2
    }
    response = test_client.post('/', data=payload)
    assert response.status_code == 200


def test_is_palindrome_post_ok(test_client):
    payload = {
        'palindrome': 'Zagwiżdż i w gaz'
    }
    response = test_client.post('/', data=payload)
    assert response.status_code == 200
    g = test_client.get('/')
    assert b"This is palindrome:" in g.data


def test_is_valid_card_post_ok(test_client):
    payload = {
        'card': '4875-2134-9491-5582'
    }
    response = test_client.post('/', data=payload)
    assert response.status_code == 200


def test_google_api_request_post_ok(test_client):
    data = {
        'search': 'hobbit'
    }
    response = test_client.post('/books', data=data)
    assert response.status_code == 200


def test_books_request_post_ok(test_client):
    response = test_client.get('/books')
    assert response.status_code == 200
    assert b"Little bit of skills for the Flyps" in response.data
    assert b"Book list" in response.data
