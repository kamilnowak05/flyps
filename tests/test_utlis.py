import pytest
import os.path

from utlis import fibonacci_calc, is_palindrome, is_valid_card, \
    create_xlsx_file, google_api_request


def test_fibonacci_calc_ok():
    assert fibonacci_calc(5) == 5


def test_fibonacci_calc_fail():
    with pytest.raises(TypeError):
        fibonacci_calc('test')


def test_is_palindrome_ok():
    assert is_palindrome('1Bo ob1') is True
    assert is_palindrome('1Doe1') is False


def test_is_valid_card_ok():
    assert is_valid_card('4875-2134-9491-5582') is True
    assert is_valid_card('4875213494915582') is True
    assert is_valid_card('9875-2134-9491-5582') is False
    assert is_valid_card('4875-2134-9491-558') is False
    assert is_valid_card('4875-2134-9491-558F') is False
    assert is_valid_card('4875:2134:9491:5582') is False


def test_google_api_request_ok():
    data = 'Hobbit'
    assert data in google_api_request(data)[0]['title']


def test_create_xlsx_file_ok():
    data = [
        {'title': 'Test',
         'author': 'John Doe',
         'published_date': '01-01-2011',
         'language': 'en',
         'price': '25.80',
         'currency': 'PLN',
         'sale_info': 'Test'}
    ]
    resp = create_xlsx_file(data)
    assert os.path.isfile('books.xlsx') is True
