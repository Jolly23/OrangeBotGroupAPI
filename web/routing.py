# -*- coding: utf-8 -*-
import views.index

routings = [
    #############################################################
    # handlers for urls
    (r"/api/urp/all_scr", views.index.UrpAllScoreInfoHandler),
]
