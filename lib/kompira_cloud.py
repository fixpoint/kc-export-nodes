# coding: UTF-8

import requests
import urllib.parse
from .helper import logger

class KompiraCloudAPI(object):

    def __init__(self, token, username=None, password=None):
        self.token = token
        self.timeout = 10
        self.request_header = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-Authorization': 'Token %s' % self.token,
        }
        if username is not None:
            self.auth = requests.auth.HTTPBasicAuth(username, password)
        else:
            self.auth = None

    def get(self, url, params=None):
        logger.info('Call API: %s %s' % (url, params))
        res = requests.get(url, params=params, headers=self.request_header, auth=self.auth, timeout=self.timeout)
        if res.status_code != 200:
            raise requests.RequestException(res.text)
        res = res.json()
        return res

    def get_items_all(self, url, limit=1000):
        offset = 0
        items = []
        while True:
            json_data = self.get(url, params={"offset": offset, "limit": limit})
            if 'items' not in json_data:
                break
            if len(json_data['items']) == 0:
                break
            items.extend(json_data['items'])
            offset += limit
            if offset > json_data['total']:
                break
        return items

    def get_api_url(self, webui_url):
        uri = urllib.parse.urlparse(webui_url)
        if uri.path.startswith('/api'):
            return webui_url
        return uri._replace(path = '/api' + uri.path).geturl()

    def get_items_from_webui_url(self, webui_url):
        url = self.get_api_url(webui_url)
        return self.get_items_all(url)
