import json
import time
from open_auth.open_auth_storage_redis_helper import OauthOpenAuthStorageRedisHelper
from open_auth.open_auth_helper import OauthOpenAuthHelper, OauthError
import yaml
import os


def get_config(key=None):
    config_file = open(os.path.join(
        "config.yaml"), encoding="UTF-8")
    config = yaml.load(config_file, Loader=yaml.FullLoader)
    if key is not None:
        return config[key]
    return config


proxies = get_config('proxies')
storage_redis_config = get_config('storage_redis')
oauth_api_config = get_config('oauth_api')
storage_redis = OauthOpenAuthStorageRedisHelper(storage_redis_config)


def update_serve_access_token(app_id: str, app_secret: str):
    server_access_token_info = storage_redis.get_server_access_token(app_id)
    run_next = True
    if server_access_token_info:
        expires_in = server_access_token_info['expires_in']
        now_time = int(time.time())
        expires_in_time = expires_in - now_time
        less_than_600 = expires_in_time > 600
        run_next = not less_than_600

    if run_next:
        auth_helper = OauthOpenAuthHelper(
            oauth_api_config, app_id, app_secret, proxies=proxies)
        try:
            server_access_token_info = auth_helper.get_server_access_token()
            storage_redis.save_server_access_token(
                app_id, server_access_token_info)
        except OauthError as error:
            print(error.response.text)


def update_js_ticket(app_id: str, app_secret: str):
    server_access_token_info = storage_redis.get_server_access_token(app_id)
    server_access_token = server_access_token_info['server_access_token']
    js_ticket_info = storage_redis.get_js_ticket(app_id)
    run_next = True
    if js_ticket_info:
        expires_in = js_ticket_info['expires_in']
        now_time = int(time.time())
        expires_in_time = expires_in - now_time
        less_than_600 = expires_in_time > 600
        run_next = not less_than_600

    if run_next:
        auth_helper = OauthOpenAuthHelper(
            oauth_api_config, app_id, app_secret, proxies=proxies)
        try:
            js_ticket_info = auth_helper.get_js_ticket(server_access_token)
            storage_redis.save_js_ticket(app_id, js_ticket_info)
        except OauthError as error:
            print(error.response.text)


def update_oauth_code(action, app_info):
    app_id = app_info['app_id']
    app_name = app_info['app_name']
    print("应用ID:%s" % app_id)
    print("应用名称:%s" % app_name)
    print("操作:%s" % action)
    app_secret = app_info['app_secret']
    if 'update_server_access_token' == action:
        update_serve_access_token(app_id, app_secret)
    elif 'update_js_ticket' == action:
        update_js_ticket(app_id, app_secret)
    else:
        print('do nothing')


def run(action):
    app_infos = get_config('app_info')
    for app_info in app_infos:
        update_oauth_code(action, app_info)
    return 'update_oauth_code'
