#!/usr/bin/env python3

from my_utility_scripts.logging_tools import log_request, my_logger

my_logger.info(f"开始运行module:{__name__}, 其文件位置在: {__file__}")

import cherrypy

from my_mako_adaptor import mako_lookup
import server_base
import articles_storage


class UnitServer(server_base.BasicServer):

    mako_template_for_server_index = "all_special_offers.html"
    SCRIPT_NAME = "all_special_offers"
    articles_structure = articles_storage.articles_structure_map[1][1]

    @cherrypy.expose
    def index(self, **template_args):
        all_articles = self.articles_structure[1]
        html_content = self.mako_template.render(
            all_articles=all_articles).strip()
        return html_content

    @cherrypy.expose
    def offer(self, name):
        mako_template = mako_lookup.get_template(name)
        html_content = mako_template.render()
        return html_content
