#!/usr/bin/env python3

from my_utility_scripts.logging_tools import log_request, my_logger
my_logger.info(f"开始运行module:{__name__}, 其文件位置在: {__file__}")

import cherrypy
from my_utility_scripts import changeDir
from my_utility_scripts.ast_analyzer import extract_ClassDefs
from my_mako_adaptor import mako_lookup
from my_cherrypy_adaptor import cherrypy_conf
import server_base


class UnitServer(server_base.BasicServer):

    mako_template_for_server_index = "team.html"
    SCRIPT_NAME = "our_team"

    @cherrypy.expose
    def consultant(self, name):
        cherrypy.log("<consultant> handler 被调用！")
        mako_template = mako_lookup.get_template('consultant.html')
        html_content = mako_template.render(name=name)
        return html_content