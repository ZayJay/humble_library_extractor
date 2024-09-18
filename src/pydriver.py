import http.cookiejar
from urllib.parse import urljoin, urlsplit
import requests
import json

URL = "https://www.humblebundle.com"
ORDER_LIST_URL = "https://www.humblebundle.com/api/v1/user/order"

ORDER_URL = "https://www.humblebundle.com/api/v1/orders?{0}"

LOGIN_URL = "https://www.humblebundle.com/login"
SIGNED_DOWNLOAD_URL = "https://www.humblebundle.com/api/v1/user/Download/{0}/sign"
STORE_URL = "https://www.humblebundle.com/store/api/humblebundle"

class PyDriver:
    def __init__(self):
        pass

    # raw output for now, then break it up : )
    def run(self):

        with open('.creds') as f:
            creds = f.read()

        (password, auth_key) = creds.split(':::::')

        # I think this is extracting the auth expiration value from the key
        # and adding time to it - assuming the value is in epoch time, this
        # should add 5 days to expiry
        expires = int(auth_key.split("|")[1]) + 60 * 60 * 24 * 5
        cookiejar = http.cookiejar.MozillaCookieJar()
        cookie = http.cookiejar.Cookie(
            version=0,
            name="_simpleauth_sess",
            value=auth_key,
            port=None,
            port_specified=False,
            domain=urlsplit(URL)[1],
            domain_specified=False,
            domain_initial_dot=False,
            path="/",
            path_specified=False,
            secure=True,
            expires=expires,
            discard=False,
            comment=None,
            comment_url=None,
            rest={},
        )
        cookiejar.set_cookie(cookie)

        print("Get list of gamekeys:")
        r = requests.get(ORDER_LIST_URL, cookies=cookiejar)
        data = json.loads(r.text.replace("\u00fc", "u"))
        print(data)

        gamekeys = []
        for datadict in data:
            gamekeys.append(datadict['gamekey'])

        print("Gamekeys....:")
        print(gamekeys)

        all_orders_url = ORDER_URL.format('all_tpkds=true&gamekeys=' + '&gamekeys='.join(gamekeys))
        print(all_orders_url)

        r = requests.get(all_orders_url, cookies=cookiejar)
        data = json.loads(r.text.replace("\u00fc", "u"))

        with open('/Users/szajac/hbrx.json', 'w') as f:
            f.write(str(data))
        f.close()
        #
        # gamekeys = dict(data).keys()
        # print("Retrieved gamekeys....")
        # print(gamekeys)