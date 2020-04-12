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
        print("No availability, checking again in 1 minute.")
        time.sleep(60)


def is_valid_cookie(cookie):
    return "ahoy_track" in cookie and "amplitude_idundefinedinstacart" in cookie


if __name__ == "__main__":
    check_availability_on_loop("shoprite","ahoy_track=true; amplitude_idundefinedinstacart.com=eyJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOm51bGwsImxhc3RFdmVudFRpbWUiOm51bGwsImV2ZW50SWQiOjAsImlkZW50aWZ5SWQiOjAsInNlcXVlbmNlTnVtYmVyIjowfQ==; _instacart_logged_in=1; __stripe_mid=954ef762-372e-45d2-98f1-dc050faf1f89; ab.storage.userId.6f8d91cb-99e4-4ad7-ae83-652c2a2c845d=%7B%22g%22%3A%2288958749%22%2C%22c%22%3A1585167584953%2C%22l%22%3A1585167584953%7D; ab.storage.deviceId.6f8d91cb-99e4-4ad7-ae83-652c2a2c845d=%7B%22g%22%3A%224bbcec4f-1405-0169-6321-9079aa3c15ba%22%2C%22c%22%3A1585167584958%2C%22l%22%3A1585167584958%7D; ajs_anonymous_id=%2224bdcb67-909f-48e5-91c1-19c52f494ef5%22; ahoy_visitor=f59e242c-5563-4037-9757-b32df8019a29; ajs_group_id=null; ajs_user_id=%2288958749%22; build_sha=390ef91ef8d2d4fca2192875b4e3a20f8b77569d; ahoy_visit=1ff6a5ea-da36-4ad8-9660-571168e66f0f; __stripe_sid=8060aa4f-fbee-4499-96e8-882490bf02e5; ab.storage.sessionId.6f8d91cb-99e4-4ad7-ae83-652c2a2c845d=%7B%22g%22%3A%2238f3bdaf-3e71-609b-3571-c467c1ff7b95%22%2C%22e%22%3A1586557443310%2C%22c%22%3A1586555643310%2C%22l%22%3A1586555643310%7D; forterToken=818c020c4ae6410999a74cf57d5449a3_1586555642584_989_UAL9_9ck; amplitude_id_b87e0e586f364c2c189272540d489b01instacart.com=eyJkZXZpY2VJZCI6ImU2NWM5NDZkLTE2OGEtNDMzMS05ZDk5LTJhZDE5ZDI1ZWJjNVIiLCJ1c2VySWQiOiI4ODk1ODc0OSIsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTU4NjU1NTY0MzgwNSwibGFzdEV2ZW50VGltZSI6MTU4NjU1NTY0NDk1NSwiZXZlbnRJZCI6MTE3MCwiaWRlbnRpZnlJZCI6MTEyLCJzZXF1ZW5jZU51bWJlciI6MTI4Mn0=; _instacart_session=ZzJMdm5EVFB5U2VsaHBpMldiQU40NUJOY1RWZ0ozeXpKNThVbThoaENwaWxTK2IxcVVyUXZSdUdtQVQyTkZnSkM2RmNkRHIwZEVpZHBQTGgrYTJmTFlZTjQ3dWZlUzVJR0YzSUNhVmY4S2hBMk5tS3lsNnBKR3llWlp2Ri9kbW5Xejh3TWR4cDZyTklFaTFPODhRaGNPeUw3SkpvNzhlNjRPdElTNkR5OThqOUptVmNmM1NBNnMyQm52N0Q4VzNJQit4LzlWdDM4K2xVL1RsTDltcFFkcURMZ3BUYnpLazdDU2NmYm1ieWt1SzIyOUZiQjJub0h4U3NKRnFiK1VYRG1VMkdoZzc0RnlXM0pXamVreXJSajRma0NHQWZ0bHd4V0hrODBQeEVpT2dPV0hHL21VejFDNGNBK2pxZFBOQ1ppK0pSZGN6Y2dmbE9Ba2xUckRZYWp3PT0tLXJkcDhTTGNlRzRoSlBxWmoxcThvcGc9PQ%3D%3D--e37940283103921bf6d7166e9cdaa2cd71ff03a5")
