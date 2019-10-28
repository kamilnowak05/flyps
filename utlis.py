import re
import requests
import json
import xlsxwriter


def fibonacci_calc(n: int) -> int:
    if n == 0:
        return 0
    b, a = 0, 1
    for i in range(1, n):
        b, a = a, a + b
    return a


def is_palindrome(word: str) -> str:
    raw_s1 = "%r" % word
    a = []
    for i in raw_s1:
        a.append(i.lower())
    word = "".join(c for c in a if c.isalnum())
    return str(word == word[::-1])


def is_palindrome_with_marks(word: str) -> str:
    raw_s1 = "%r" % word
    raw_s1 = raw_s1.replace('x0', '')
    raw_s1 = raw_s1.replace(' ', '')
    a = []
    for i in raw_s1:
        a.append(i.lower())
    return str(a == a[::-1])


def is_valid_card(numb: str) -> str:
    """ Return True if sequence is a valid card number.

        It must contain exactly 16 digits.
        It must start with a 4,5 or 6
        It must only consist of digits (0-9).
        It may have digits in groups of 4 , separated by one hyphen "-".
        It must NOT use any other separator like ' ' , '_', etc."""

    pattern = '^([456][0-9]{3})-?([0-9]{4})-?([0-9]{4})-?([0-9]{4})$'
    match = re.fullmatch(pattern, numb)
    if match is None:
        return False
    return True


def google_api_request(search):
    response = requests.get(
        f"https://www.googleapis.com/books/v1/volumes?q={search}+intitle:{search}"
    )
    resp = json.loads(response.text)
    books = []
    book = {}
    if 'items' in resp:
        for i in resp['items']:
            book['title'] = i['volumeInfo'].get('title')
            book['author'] = i['volumeInfo'].get('authors', 'N/A')
            book['language'] = i['volumeInfo'].get('language', 'N/A')
            book['published_date'] = i['volumeInfo'].get('publishedDate', 'N/A')
            book['sale_info'] = i['saleInfo'].get('saleability', 'N/A')
            if 'listPrice' in i['saleInfo']:
                book['price'] = str(i['saleInfo']['listPrice'].get('amount', 'N/A'))
                book['currency'] = i['saleInfo']['listPrice'].get('currencyCode', 'N/A')
            else:
                book['price'] = 'N/A'
                book['currency'] = 'N/A'
            books.append(dict(book))
    return books


def create_xlsx_file(data):
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook('books.xlsx')
    worksheet = workbook.add_worksheet()

    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': 1})

    # Setting text align to top and text wrap.
    cell_format = workbook.add_format({'text_wrap': True})
    cell_format.set_align('top')

    # Adjust the column width.
    worksheet.set_column(0, 0, 4)
    worksheet.set_column(1, 1, 45)
    worksheet.set_column(2, 3, 15)
    worksheet.set_column(4, 7, 9)

    # Write some data headers.
    worksheet.write('A1', 'No.', bold)
    worksheet.write('B1', 'Title', bold)
    worksheet.write('C1', 'Author', bold)
    worksheet.write('D1', 'Published date', bold)
    worksheet.write('E1', 'Lang', bold)
    worksheet.write('F1', 'Price', bold)
    worksheet.write('G1', 'Currency', bold)
    worksheet.write('H1', 'For Sale', bold)

    # Start from the first cell below the headers.
    row = 1
    col = 0
    no = 1

    for i in data:
        worksheet.write_string(row, col, f'{no}.')
        worksheet.write_string(row, col + 1, i['title'], cell_format)
        worksheet.write_string(row, col + 2, i['author'][0], cell_format)
        worksheet.write_string(row, col + 3, i['published_date'])
        worksheet.write_string(row, col + 4, i['language'])
        worksheet.write_string(row, col + 5, i['price'])
        worksheet.write_string(row, col + 6, i['currency'])
        worksheet.write_string(row, col + 7, i['sale_info'])
        row += 1
        no += 1

    workbook.close()
    return workbook
