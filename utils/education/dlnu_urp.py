# -*- coding: utf-8 -*-
import base64
import os
import random
import re
import sqlite3
import time
from hashlib import md5
from multiprocessing.dummy import Pool
from urlparse import urljoin

import psycopg2
import requests
from bs4 import BeautifulSoup

from settings import URP_URL, PHONE_NUMBER_DB_PATH, PG_DATABASE_INFO, PG_DATABASE_INFO_2
from sql import *
from utils.const import TIME_OUT

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


class UrpDb(object):
    @classmethod
    def get_all_score(cls, uid, passwd):
        data = cls.exc_sql(all_score_sql, (uid,), fetch_type=2)
        data.sort(key=lambda keys: keys[8])
        score_list = []
        for subject in data:
            if subject[0] == '001':
                course_score = subject[5]
            elif subject[0] == '002':
                course_score = subject[6]
            else:
                continue
            exam_info = {
                'course_num': subject[1],
                'course_order': subject[2],
                'course_name': subject[3],
                'course_credit': subject[4],
                'course_score': course_score,
                'course_type': subject[7]
            }
            score_list.append(exam_info)
        return score_list
