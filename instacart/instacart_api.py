import requests
import json
import time
import datetime

base_domain = "https://www.instacart.com"
no_time_available_title = "No delivery times available"


def get_availability_json(store,cookie):
    suffix = "/v3/containers/" + store + "/next_gen/retailer_information/content/delivery?source=web"
    url = base_domain + suffix
    r = requests.get(url, headers=headers(cookie))
    if r.status_code >= 400:
        print(r.text)
        raise Exception(r)
    else:
        return json.loads(r.text)


def headers(cookie):
    headers = {}
    headers["cookie"] = cookie
    headers["user-agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
    return headers


def is_there_availability(r):
    try:
        data = r["container"]["modules"][0]["data"]
        if data["title"] == no_time_available_title:
            return False
    except:
        return True
    return True


def check_availability(store,cookie):
    available = is_there_availability(get_availability_json(store,cookie))
    if available:
        print("Found availability at: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("No availability, checking again in 1 minute.")


def check_availability_on_loop(store,cookie):
    while True:
        available = is_there_availability(get_availability_json(store,cookie))
        if available:
            print("Found availability at: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            break
        print("No availability, checking again in 30 seconds.")
        time.sleep(30)


def is_valid_cookie(cookie):
    return "ahoy" in cookie and "amplitude_idundefinedinstacart" in cookie


if __name__ == "__main__":
    check_availability_on_loop("shoprite","")
