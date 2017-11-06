# -*- coding: utf-8 -*-
from abc import abstractmethod

import base
from utils.education.dlnu_urp import GetScore


class UrpAllScoreInfoHandler(base.BaseHandler):
    @abstractmethod
    def post(self):
        self.acquire_data(
            class_object=UrpDb,
            args={'uid': 'uid', 'passwd': 'passwd'},
            verify_method='verify_urp_password',
            exc_method='get_all_score',
            args_init=False,
            cache=60 * 24
        )
