import requests
import hashlib
import sys


def request_api_data (query):
    url = "https://api.pwnedpasswords.com/range/" + query

    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError("error")
    return response

def get_leaks_count (list, tail):
    hashes = (line.split(":") for line in list.text.splitlines())
    for h, count in hashes:
        if h == tail:
            return (count)
    return 0

def api_check (password):
    hash_pass = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    first_5 = hash_pass[:5]
    tail = hash_pass[5:]
    response = request_api_data(first_5)
    return get_leaks_count(response, tail)

def main (args):
    for password in args:
        count = api_check(password)
        if count:
            print (f'{password} was found {count} times! Maybe change it..')
        else:
            print (f'{password} was not found! Good Password!')


main (sys.argv[1:])