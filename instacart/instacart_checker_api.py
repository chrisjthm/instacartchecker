import requests

instacart_checker_api_url = "https://instacart-checker-api.herokuapp.com"


def check_and_notify(store, phone_number, cookie):
    url = instacart_checker_api_url + "/checkAndNotify"
    payload = "{\"phoneNumber\":\"" + phone_number + "\", \"store\": \"" + store + "\"}"
    headers = {"Content-Type": "application/json", "X-Cookie": cookie}
    print(headers)
    r = requests.post(url, headers=headers, data=payload)
    return r
