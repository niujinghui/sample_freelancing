#!/usr/bin/env python3

from my_utility_scripts.logging_tools import my_logger

my_logger.info(f"开始运行module:{__name__}, 其文件位置在: {__file__}")

import cherrypy
import os
import functools
import collections
import json
import threading
import sqlalchemy
from sqlalchemy.orm import aliased
import pprint
import time

from my_mako_adaptor import mako_lookup
from my_utility_scripts.chronology import UniversalTimePoint


def uses_json(func):
    @functools.wraps(func)
    @cherrypy.tools.accept(media="application/json")
    def wrapper(*args, **kwargs):
        cherrypy.serving.response.headers['Content-Type'] = "application/json"
        kwargs = dict(kwargs)
        try:
            body = cherrypy.request.body.read()
            kwargs.update(json.loads(body))
        except TypeError:
            pass
        return json.dumps(func(*args, **kwargs)).encode('utf8')

    return wrapper


# for the long-polls
longpoll_blockers_channel = {}


class BasicServer:
    ''' 
        含有：mako_template, index
        无任何backend的功能设置，作为base class, 需要subclass，添加有用的 request handlers。
    '''

    mako_template_for_server_index = ''

    def __init__(self):
        self.mako_template = mako_lookup.get_template(
            self.mako_template_for_server_index)
        self.human_readable_server_name = getattr(
            self.mako_template.module, "human_readable_server_name", None)

    @cherrypy.expose
    def index(self, **template_args):
        html_content = self.mako_template.render(
            template_args=template_args).strip()
        return html_content


# for long running service termination purpose:
def kill_child_threads():
    my_logger.info(f"<kill_child_threads> 被调用！")
    for classmodel, blocker in longpoll_blockers_channel.items():
        blocker.running_status = "termination"
        blocker.set()
        cherrypy.log(f"正在结束{classmodel}的long polling...")


my_logger.info(f"{__name__} 运行到尾部。")
