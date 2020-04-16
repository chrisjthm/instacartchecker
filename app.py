from instacart import instacart_checker_api
from flask import Flask, render_template, request, Response, redirect

app = Flask(__name__)

redirect_url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        store = request.form['store']
        cookie = request.form['cookie']
        phone_number = request.form['phone_number']
        return check(store, cookie, phone_number)
    return render_template("home.html")


@app.route('/check')
def check(store, cookie, phone_number):
    if not phone_number.startswith("+1") and len(phone_number) == 10:
        phone_number = "+1" + phone_number
    elif len(phone_number) == 11:
        phone_number = "+" + phone_number
    r = instacart_checker_api.check_and_notify(store, phone_number, cookie)
    if r.status_code >= 400:
        return "Oops, there was an error:\n" + r.text
    else:
        return "Hooray! We received your request. We will text you when we find something."


if __name__ == '__main__':
    app.run(host= '0.0.0.0', debug=True)