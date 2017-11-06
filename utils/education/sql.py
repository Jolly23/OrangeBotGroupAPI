# -*- coding: utf-8 -*-
from datetime import datetime

import cx_Oracle

from settings import ORL_DATABASE_URI


def connect():
    dsn_tns = cx_Oracle.makedsn(*ORL_DATABASE_URI[:3])
    conn = cx_Oracle.connect(ORL_DATABASE_URI[-2], ORL_DATABASE_URI[-1], dsn_tns)
    return conn

# 验证Urp密码
get_password_sql = '''select MM from TONGYI.T_YHMMB where ZJH = :1'''

# 学生个人课程
s_courses_sql = '''select KCM, NEWJW.CODE_KCB.KCH, KXH, SKZC, SKXQ, SKJC , XQM, JXLM, JASM
from NEWJW.XK_XKB_SJDD_VIEW, NEWJW.CODE_KCB
where NEWJW.XK_XKB_SJDD_VIEW.XH = :1 and
NEWJW.XK_XKB_SJDD_VIEW.KCH = NEWJW.CODE_KCB.KCH and
ZXJXJHH = :2'''
