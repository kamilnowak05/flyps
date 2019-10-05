import os
from utlis import fibonacci_calc, is_palindrome, is_valid_card, \
    google_api_request, create_xlsx_file, is_palindrome_with_marks
from flask import Flask, render_template, request, send_file


app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        if 'fibonacci' in request.form:
            fib = request.form['fibonacci']
            fib = int(fib)
            if fib < 0:
                return render_template(
                    'index.html',
                    result_fib='It can\'t be negative number.'
                )
            result = fibonacci_calc(fib)
            return render_template('index.html', result_fib=str(result))

        elif 'palindrome' in request.form:
            pal = request.form['palindrome']
            result = is_palindrome(pal)
            if result is False:
                result = 'False'
            return render_template('index.html', result_palin=result)

        elif 'palindrome_with_marks' in request.form:
            pal = request.form['palindrome_with_marks']
            result = is_palindrome_with_marks(pal)
            if result is False:
                result = 'False'
            return render_template('index.html', result_palin_marks=result)

        elif 'card' in request.form:
            numb = request.form['card']
            result = is_valid_card(numb)
            if result:
                result = 'Yes'
            else:
                result = 'No'
            return render_template('index.html', result_card=result)


@app.route('/books', methods=['POST', 'GET'])
def books():
    if request.method == 'GET':
        return render_template('books.html')
    if request.method == 'POST':
        search = request.form['search']
        response = google_api_request(search)
        create_xlsx_file(response)
        return send_file('books.xlsx', as_attachment=True)


if __name__ == '__main__':
    app.run()
