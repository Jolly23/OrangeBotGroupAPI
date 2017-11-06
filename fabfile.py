# -*- coding: utf-8 -*-
import os

from fabric.api import cd, local

da_dir = os.path.abspath(os.path.dirname(__file__))


def deploy_wechaty_group_api():
    with cd(da_dir):
        local('git pull --rebase origin feature-new-security')
        local('supervisorctl -c deploy_conf/supervisor.conf restart apiapp:')


def restart_wechaty_group_api():
    with cd(da_dir):
        local('supervisorctl -c deploy_conf/supervisor.conf restart apiapp')
