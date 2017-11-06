# -*- coding: utf-8 -*-
import json
import time
from datetime import datetime
from hashlib import md5

import psycopg2
import redis
import tornado.web

from settings.config import USER_KEYS, REDIS_DB_URL, PG_DATABASE_INFO
from tools import get_sha1, check_args_sign, sign, decrypt, encrypt, get_cache, set_cache, api_log_sys
from utils.const import ERRMSG
from utils.dump_json import build_json, build_json2


class BaseHandler(tornado.web.RequestHandler):
    def write_json(self, **kwargs):
        return self.write(build_json(**kwargs))

    @staticmethod
    def encrypt_msg(status_code, secret_key, data):
        args_sign = sign(secret_key, data['data'] if data.get('data') else {})
        re_data = {
            'timestamp': int(time.time()),
            'errcode': status_code,
            'errmsg': ERRMSG.get(status_code),
        }
        if status_code == 0:
            re_data['args_sign'] = args_sign
            re_data['encrypt_msg'] = encrypt(secret_key, args_sign, build_json2(**data))
        return re_data

    def security_check(self, func_args, optional_args, apply_method):
        compulsory_query_arguments = ['timestamp', 'nonce', 'msg_signature']
        compulsory_body_arguments = ['encrypt_msg', 'args_sign', 'api_key']
        query_dict = {}
        body_dict = {}
        for needed_query in compulsory_query_arguments:
            query_dict[needed_query] = self.get_query_argument(needed_query, None)
        for needed_body in compulsory_body_arguments:
            body_dict[needed_body] = self.get_body_argument(needed_body, None)
        if None in query_dict.values():
            return -40001, None
        if None in body_dict.values():
            return -40002, None
        if len(query_dict['nonce']) < 10 or len(query_dict['nonce']) > 32:
            return -40003, None
        ret, request_sign = get_sha1(query_dict['timestamp'], query_dict['nonce'], body_dict['encrypt_msg'],
                                     body_dict['args_sign'], body_dict['api_key'])
        if ret != 0:
            return ret, None
        if query_dict['msg_signature'] != request_sign:
            return -40004, None
        api_user = NEW_USER_KEYS.get(body_dict['api_key'])
        if not api_user:
            return -40005, None
        if apply_method and apply_method not in api_user['PERMITTED_API']:
            return -40021, None
        ret, post_args = decrypt(api_user['SECRET_KEY'], body_dict['args_sign'], body_dict['encrypt_msg'])
        if ret != 0:
            return ret, None
        if not check_args_sign(query_dict['nonce'], post_args, body_dict['args_sign']):
            return -40006, None
        if not isinstance(post_args, dict):
            return -40007, None

        if not set(post_args.keys()) >= set(func_args.values()) or \
                not set(post_args.keys()) <= set(func_args.values()) | set(optional_args.values()):
            return -40008, None

        for each_key, each_value in func_args.items():
            if each_key != each_value:
                post_args[each_key] = post_args.pop(each_value)

        post_args['SECRET_KEY'] = api_user['SECRET_KEY']
        post_args['API_KEY'] = body_dict['api_key']
        return 0, post_args

    def acquire_data(self, class_object, args=None, optional_args=None,
                     verify_method=None, exc_method=None, args_init=True, cache=None):
        re_info = None
        is_cache_data = None

        status_code, args = self.security_check(
            args if args else {}, optional_args if optional_args else {}, exc_method
        )
        api_key, secret_key = (args.pop('API_KEY'), args.pop('SECRET_KEY')) if status_code == 0 else (None, None)
        key_name = u'API_CACHE_({}.{})_{}'.format(class_object.__name__, exc_method, md5(str(args)).hexdigest())
        if cache and status_code == 0:
            re_info = get_cache(key_name)
            if re_info:
                is_cache_data = True
        if not re_info and status_code == 0:
            is_cache_data = False
            instanced_class = class_object(**args) if args_init else class_object()
            if verify_method:
                status_code = getattr(instanced_class, verify_method)() \
                    if args_init else getattr(instanced_class, verify_method)(**args)
            if exc_method and status_code == 0:
                re_info = getattr(instanced_class, exc_method)() \
                    if args_init else getattr(instanced_class, exc_method)(**args)
                if re_info and cache:
                    set_cache(key_name, re_info, cache)
        data = dict(
            errcode=status_code,
            errmsg=ERRMSG.get(status_code),
        )
        if re_info:
            data['data'] = re_info

        ##############
        # LOG SYS
        api_log_sys(
            args, u'{0}.{1}'.format(class_object.__name__, exc_method),
            status_code, api_key, data, dict(self.request.headers.items()), is_cache_data
        )
        ##############

        self.write_json(**self.encrypt_msg(status_code, secret_key, data))




    # CREATE TABLE api_logs(
    #   id serial PRIMARY KEY,
    # 	method_name TEXT NOT NULL,
    # 	status_code INT NOT NULL,
    # 	api_user varchar(128) not null,
    # 	args json,
    # 	re_data json,
    # 	headers json,
    # 	is_cache_data boolean,
    # 	time timestamp not null default CURRENT_TIMESTAMP + interval '8 hours'
    # );
