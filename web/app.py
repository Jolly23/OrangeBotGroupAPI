# -*- coding: utf-8 -*-
import tornado.httpserver
import tornado.ioloop
import tornado.log
import tornado.options
import tornado.web
from tornado.log import logging
from tornado.options import define, options

import routing
from settings import *

#############################################################
#  command line options

define("port", default=API_SITE_PORT, help="run on the given port", type=int)  # port number
define("ip_address", default=API_SITE_IPADDRESS, help="run on the given ip_address", type=str)  # port number
define("debug_template", default=0, help="display template input data", type=int)  # template debug option


class Application(tornado.web.Application):

    def __init__(self):

        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), API_TEMPLATE_PATH),
            static_path=os.path.join(os.path.dirname(__file__), API_STATIC_PATH),
            static_urls={
                'js': API_JS_URL,
                'css': API_CSS_URL,
                'img': API_IMG_URL,
            },

            site_path=API_SITE_PATH,
            xsrf_cookies=API_XSRF_COOKIES,
            cookie_secret=API_SECRET_KEY,
            session_timeout=API_SESSION_TIMEOUT,
            login_url=API_LOGIN_URL,
            autoescape=API_AUTOESCAPE,
            debug=API_DEBUG_MODE,

        )
        super(Application, self).__init__(routing.routings, **settings)


def main():

    tornado.options.log_file_prefix = API_LOG_FILE   # set log file
    tornado.options.options.logging = "debug"   # set log level
    tornado.options.parse_command_line()

    try:
        '''start server 启动服务'''
        application = Application()
        application.settings['DEBUG_TEMPLATE'] = tornado.options.options.debug_template

        logging.info("Start %s HTTP server on port: %d ...\n\n" % ('DA api web', options.port))
        http_server = tornado.httpserver.HTTPServer(application, xheaders=True)
        http_server.listen(port=options.port, address=options.ip_address)
        tornado.ioloop.IOLoop.instance().start()

    except Exception as e:
        # start server fail
        logging.error('Failed to start HTTP server, due to : %s' % e)
        logging.error("HTTP server is terminated.")

if __name__ == "__main__":
    main()
