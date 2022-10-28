#!/usr/bin/env python3

from my_utility_scripts.logging_tools import log_request, my_logger

my_logger.info(f"开始运行module:{__name__}, 其文件位置在: {__file__}")

import cherrypy

from my_mako_adaptor import mako_lookup
import server_base
import articles_storage


class UnitServer(server_base.BasicServer):

    mako_template_for_server_index = "our_perspectives.html"
    SCRIPT_NAME = "our_perspectives"
    articles_structure = articles_storage.articles_structure_map[1][0]

    @cherrypy.expose
    def index(self, **template_args):
        html_content = self.mako_template.render(
            articles_structure=self.articles_structure).strip()
        return html_content

    @cherrypy.expose
    def perspective_article(self, article_identifier):
        nt = articles_storage.NodeTraversal()
        path = nt.get_path(
            article_identifier,
            head_node=articles_storage.get_node("our_perspectives"))
        article_subcategory = path[2][0]
        article_title = path[-1][1]["article_title"]
        articles_list_under_this_subcategory = path[-2][1]
        mako_template = mako_lookup.get_template(article_identifier)
        html_content = mako_template.render(
            article_identifier=article_identifier,
            article_subcategory=article_subcategory,
            article_title=article_title,
            articles_list_under_this_subcategory=
            articles_list_under_this_subcategory)
        return html_content

    @cherrypy.expose
    def perspective_subcategory(self, subcategory_name):
        mako_template = mako_lookup.get_template('perspective_category.html')
        subcategory_node = articles_storage.get_node(subcategory_name)
        html_content = mako_template.render(subcategory_name=subcategory_name,
                                            subcategory_node=subcategory_node)
        return html_content
