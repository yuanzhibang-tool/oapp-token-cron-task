# /usr/bin/python3
import requests
import sys


class OauthError(Exception):

    def __init__(self, code, message, response):
        self.code = code
        self.message = message
        self.response = response


class OauthNetworkError(OauthError):
    pass


class OauthApiError(OauthError):
    pass


class OauthOpenAuthHelper(object):

    GET_SERVER_ACCESS_TOKEN_URL=None
    GET_USER_ACCESS_TOKEN_URL=None
    GET_JS_TICKET_URL =None
    REFRESH_USER_TOKEN_URL =None

    app_id = ''
    secret = ''
    proxies = None

    def __init__(self, config, app_id, secret, proxies=None):

        self.GET_SERVER_ACCESS_TOKEN_URL = config['get_server_access_token_url']
        self.GET_USER_ACCESS_TOKEN_URL = config['get_user_access_token_url']
        self.GET_JS_TICKET_URL = config['get_js_ticket_url']
        self.REFRESH_USER_TOKEN_URL = config['refresh_user_token_url']

        self.app_id = app_id
        self.secret = secret
        self.proxies = proxies

    def post(self, url, data):
        response = requests.post(url=url, data=data, proxies=self.proxies)
        self.raise_network_error(response)
        self.raise_api_error(response)
        response_object = response.json()
        return response_object['data']

    def raise_network_error(self, response):
        status_code = response.status_code
        print("raise_network_error:status:%d" % status_code)
        if status_code != 200:
            raise OauthNetworkError(status_code, '', response)

    def raise_api_error(self, response):
        response_object = response.json()
        status = response_object['status']
        message = response_object['message']
        print("raise_api_error:status:%s" % status)
        print("raise_api_error:message:%s" % message)
        if status != '2000':
            raise OauthApiError(status, message, response)

    def get_server_access_token(self):
        post_data = {
            'app_id': self.app_id,
            'secret': self.secret,
            'grant_type': 'client_credential'
        }
        return self.post(self.GET_SERVER_ACCESS_TOKEN_URL, post_data)

    def get_js_ticket(self, access_token):
        post_data = {
            'app_id': self.app_id,
            'access_token': access_token,
            'type': 'js_ticket'
        }
        return self.post(self.GET_JS_TICKET_URL, post_data)

    def get_user_access_token(self, code):
        post_data = {
            'app_id': self.app_id,
            'secret': self.secret,
            'grant_type': 'authorization_code',
            'code': code
        }
        return self.post(self.GET_USER_ACCESS_TOKEN_URL, post_data)

    def refresh_user_token(self, user_access_token_info):
        openId = user_access_token_info['open_id']
        refreshToken = user_access_token_info['refresh_token']
        post_data = {
            'app_id': self.app_id,
            'grant_type': 'refresh_token',
            'open_id': openId,
            'refresh_token': refreshToken
        }
        return self.post(self.REFRESH_USER_TOKEN_URL, post_data)
