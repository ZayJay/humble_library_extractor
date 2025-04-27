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

        print("Get gamekey details:")
        all_orders_url = ORDER_URL.format('all_tpkds=true&gamekeys=' + '&gamekeys='.join(gamekeys))
        print(all_orders_url)

        r = requests.get(all_orders_url, cookies=cookiejar)
        data = json.loads(r.text.replace("\u00fc", "u"))

        with open('/Users/szajac/hbrx.json', 'w') as f:
            f.write(str(data))
        f.close()

        key_details = {}
        for gamekey in data.keys():
            key_details[gamekey] = {}
            key_details[gamekey]['product'] = {}
            key_details[gamekey]['product']['machine_name'] = data[gamekey]['product']['machine_name']
            key_details[gamekey]['product']['human_name'] = data[gamekey]['product']['human_name']
            key_details[gamekey]['subproducts'] = []
            if 'subproducts' in data[gamekey]:
                for subproduct in data[gamekey]['subproducts']:
                    subproduct_details = {}
                    subproduct_details['human_name'] = subproduct['human_name']
                    subproduct_details['machine_name'] = subproduct['machine_name']

                    subproduct_details['downloads'] = {}
                    for download in subproduct['downloads']:
                        download_struct = download['download_struct']
                        for ds in download_struct:
                            if 'name' not in ds:
                                subproduct_details['downloads']['status'] = 'Download \'name\' not found'
                            else:
                                if ds['name'] not in subproduct_details['downloads']:
                                    subproduct_details['downloads'][ds['name']] = {}
                                    subproduct_details['downloads'][ds['name']]['web_url'] = ds['url']['web']
                                    subproduct_details['downloads'][ds['name']]['sha1'] = safe_get_key(ds, 'sha1')
                                    subproduct_details['downloads'][ds['name']]['md5'] = safe_get_key(ds, 'md5')
                                    subproduct_details['downloads'][ds['name']]['file_size'] = safe_get_key(ds, 'file_size')
                                    subproduct_details['downloads'][ds['name']]['human_size'] = safe_get_key(ds, 'human_size')
                                    subproduct_details['downloads'][ds['name']]['small'] = safe_get_key(ds, 'small')

                    key_details[gamekey]['subproducts'].append(subproduct_details)

        with open('/Users/szajac/key_details.txt', 'w') as f:
            f.write(str(data))
        f.close()

def safe_get_key(dict, key):
    if key in dict:
        return dict[key]
    else:
        return "Key '{0}' not found".format(key)