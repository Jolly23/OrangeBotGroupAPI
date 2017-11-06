# -*- coding: utf-8 -*-

import binascii
import sys
from hashlib import md5, sha1

import redis
from Crypto.Cipher import AES

from settings.config import REDIS_DB_URL

reload(sys)
sys.setdefaultencoding('utf-8')


def get_cache(key_name):
    conn = redis.Redis(**REDIS_DB_URL)
    re_value = conn.get(key_name)
    if re_value:
        return eval(re_value)


def set_cache(key_name, re_info, cache_time):
    conn = redis.Redis(**REDIS_DB_URL)
    try:
        conn.set(name=key_name, value=re_info, ex=int(60 * cache_time))
        return True
    except redis.ConnectionError, redis.ResponseError:
        return False


def get_sha1(*args):
    try:
        sort_list = map(lambda x: str(x), args)
        sort_list.sort()
        sha = sha1()
        sha.update("".join(sort_list))
        return 0, sha.hexdigest().upper()
    except Exception, e:
        return -40011, None


def encrypt(secret_key, encrypt_sign, raw):
    key = md5('{secret_key}'.format(secret_key=secret_key)).digest()
    iv = md5(encrypt_sign).digest()
    raw += (16 - len(raw) % 16) * '\0'
    generator = AES.new(key, AES.MODE_CBC, IV=iv)
    return binascii.b2a_hex(generator.encrypt(raw))


def decrypt(decrypt_key, encoding_aes_key, enc):
    key = md5(decrypt_key).digest()
    iv = md5(encoding_aes_key).digest()
    enc = binascii.unhexlify(enc)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    try:
        return 0, eval(cipher.decrypt(enc).decode('utf-8').rstrip("\0"))
    except (SyntaxError, NameError, UnicodeDecodeError), e:
        return -40012, None


def to_utf8(raw):
    return raw.encode("utf-8") if isinstance(raw, unicode) else raw


def sign(string, raw):
    method_list = isinstance(raw, list)
    if isinstance(raw, dict):
        for each_value in raw.values():
            if isinstance(each_value, (list, dict)):
                method_list = True
                break
    if method_list:
        s = 'count=' + str(len(raw))
    else:
        raw = [(k, str(raw[k]) if isinstance(raw[k], (int, float)) else raw[k]) for k in sorted(raw.keys())]
        s = "&".join("=".join(kv) for kv in raw if kv[1])
    s += "&string={0}".format(string)
    return md5(to_utf8(s)).hexdigest().upper()


def check_args_sign(nonce, raw, args_sign):
    return sign(nonce, raw) == args_sign


def api_log_sys(args, method_name, status_code, api_key, data, headers, is_cache_data):
    if args:
        for each_secret_arg in ['password', 'passwd', 'newpass']:
            if each_secret_arg in args:
                args[each_secret_arg] = '***keep_secret***'
    record = {
        'method_name': method_name,
        'status_code': status_code,
        'api_user': USER_KEYS[api_key]['SYS_NAME'] if USER_KEYS.get(api_key) else api_key,
        'args': json.dumps(args if args else {}),
        're_data': json.dumps(data),
        'headers': json.dumps(headers),
        'timestamp': time.time(),
        'is_cache_data': is_cache_data,
    }

    log_list_name = 'NEW_API_SYSTEM_LOGS_CACHE'
    conn = redis.Redis(**REDIS_DB_URL)
    conn.rpush(log_list_name, record)
