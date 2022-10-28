#!/usr/bin/env python3

import logging
# logging.basicConfig(filename='./mylog.txt',
# format='%(asctime)s [%(threadName)s: %(thread)d] %(message)s', filemode='w', level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(threadName)s %(thread)d %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %I:%M:%S %p')
my_logger = logging.getLogger()
my_logger.info("开始运行module:{}, 其文件位置在: {}".format(__name__, __file__))

import functools
import cherrypy

import traceback


def logging_callstacks():
    for line in traceback.format_stack():
        my_logger.info(line.strip())


def stringify_attrs(obj):
    """docstring for stringify_attrs"""
    attrs = vars(obj)
    return ',\n'.join("%s: %s" % item for item in attrs.items())


def log_request(func):
    @functools.wraps(func)
    def wrapper_func(*arg, **kw):
        cherrypy.log("Logging from <log_request> decorator...")
        cherrypy.log("<cherrypy.request>ID是：{}".format(id(cherrypy.request)))
        cherrypy.log("<cherrypy.request>的情况是：\n{}".format(
            stringify_attrs(cherrypy.request)))
        cherrypy.log("<cherrypy.request.body>的情况是：{}".format(
            stringify_attrs(cherrypy.request.body)))
        return func(*arg, **kw)

    return wrapper_func
