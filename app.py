from flask import Flask
from playsound import playsound
from instacart import instacart_api
from flask import Flask, render_template, request, Response
from datetime import datetime
import time
app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        store = request.form['store']
        cookie = request.form['cookie']
        return check(store, cookie)
    return render_template("home.html")


@app.route('/check')
def check(store, cookie):
    if cookie:
        def check_on_loop():
            while True:
                if not instacart_api.is_valid_cookie(cookie):
                    yield "Not valid cookie, please look at instructions and try again!"
                    break
                try:
                    available = instacart_api.is_there_availability(instacart_api.get_availability_json(store,cookie))
                except:
                    yield "Oops! Something went wrong. Please go back, check instructions, and try again"
                    break
                timenow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if available:
                    playsound("airhorn.mp3")
                    yield "Found availability at: " + timenow + \
                          "\nIf you think this is wrong, please recheck store name and try again"
                    break
                yield "No availability at " + timenow + ", checking again in 1 minute.\n"
                time.sleep(60)
        return Response(check_on_loop(), content_type='text/event-stream')



@app.route('/test_sound')
def test_sound():
    playsound("instacart/airhorn.mp3")


if __name__ == '__main__':
    app.run(host= '0.0.0.0', debug=False)