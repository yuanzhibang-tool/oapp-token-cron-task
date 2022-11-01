# /usr/bin/python3
# -*- coding: utf-8 -*-

import time
import redis
import json


class OauthOpenAuthStorageRedisHelper(object):

    def __init__(self, config):
        self.host = config['host']
        self.port = config['port']
        self.auth = config['auth']
        self.db = config['db']
        self.client = redis.Redis(
            host=self.host, port=self.port, password=self.auth, db=self.db, decode_responses=True)

    # 从数据库获取有效的server_access_token
    def get_server_access_token(self, app_id):
        server_access_token_info_string = self.client.get(
            self.get_app_server_access_token_key(app_id))
        if server_access_token_info_string:
            server_access_token_info = json.loads(
                server_access_token_info_string)
            if server_access_token_info:
                return server_access_token_info
        return False

    # 保存server_access_token数据到本地数据库
    def save_server_access_token(self, app_id, server_access_token_info):
        server_access_token = server_access_token_info['access_token']
        now_time = int(time.time())
        code_expires_in = server_access_token_info['expires_in']
        expires_in = server_access_token_info['expires_in'] + now_time
        save_dict = {
            "server_access_token": server_access_token,
            "expires_in": expires_in
        }
        save_dict_string = json.dumps(save_dict)
        self.client.set(self.get_app_server_access_token_key(app_id),
                        save_dict_string, code_expires_in)
        # 从数据库获取有效的js_ticket

    def get_js_ticket(self, app_id):
        js_ticket_info_string = self.client.get(
            self.get_app_js_ticket_key(app_id))
        if js_ticket_info_string:
            js_ticket_info = json.loads(js_ticket_info_string)
            if js_ticket_info:
                return js_ticket_info
        return False

    # 保存js_ticket到数据库
    def save_js_ticket(self, app_id, js_ticket_info):
        js_ticket = js_ticket_info['ticket']
        now_time = int(time.time())
        code_expires_in = js_ticket_info['expires_in']
        expires_in = js_ticket_info['expires_in'] + now_time
        save_dict = {
            "js_ticket": js_ticket,
            "expires_in": expires_in
        }
        save_dict_string = json.dumps(save_dict)
        self.client.set(self.get_app_js_ticket_key(app_id),
                        save_dict_string, code_expires_in)

    # 从数据库获取即将失效的user_access_token

    def get_app_server_access_token_key(self, app_id):
        return "type/server_access_token_info/app_id/%s" % app_id

    def get_app_js_ticket_key(self, app_id):
        return "type/js_ticket_info/app_id/%s" % app_id

    def close_connection(self):
        self.client.close()
