# -*- coding: utf-8 -*-
import json


def build_json(errcode, errmsg, data=None):
    ret = {
        'errcode': errcode,
        'errmsg': errmsg,
    }
    if data:
        ret['data'] = data

    return json.dumps(ret)


def build_json2(**kwargs):
    return json.dumps(kwargs)
