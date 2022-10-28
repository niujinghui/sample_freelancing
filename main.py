#!/usr/bin/env python3

from my_utility_scripts.logging_tools import log_request, my_logger

my_logger.info(f"开始运行module:{__name__}, 其文件位置在: {__file__}")

import cherrypy
import json
import os
import glob
import importlib

from my_utility_scripts import changeDir
from my_utility_scripts.ast_analyzer import extract_ClassDefs
from my_mako_adaptor import mako_lookup
from my_cherrypy_adaptor import cherrypy_conf
import server_base
import articles_storage


# root server:
class MDRT(server_base.BasicServer):

    mako_template_for_server_index = "homepage.html"

    def __init__(self):
        super().__init__()
        self.unitservers_index = {}
        self._collect_subunit_servers()

    def _collect_subunit_servers(self):
        """
            use ast to parse and collect UnitServer modules, when a .py file with both:
                - <UnitServer> class;
                - SCRIPT_NAME
        """
        my_logger.info('现在开始搜集 subunit servers!')
        relative_path = os.path.dirname(__file__)
        with changeDir(relative_path):
            py_files_list = glob.glob("*.py")
            my_logger.info(f"我发现的所有待测试services有：{py_files_list}")
            # 检查每个.py文件，看是否符合2个标准:
            for pf in py_files_list:
                with open(pf, "r") as source:
                    target = extract_ClassDefs(
                        source_file_content=source.read(),
                        classname="UnitServer",
                        hasClassAttr="SCRIPT_NAME")
                if target:
                    module_name = pf.replace('.py', '')
                    unit_server = importlib.import_module(
                        module_name).UnitServer()
                    # add an unit branch to root server, which is 'self':
                    setattr(self, target['SCRIPT_NAME'], unit_server)
                    # add to unitservers_index:
                    self.unitservers_index[
                        '/' +
                        module_name] = unit_server.human_readable_server_name
        my_logger.info('搜集 subunit servers 完毕!')

    @cherrypy.expose
    def about(self):
        mako_template = mako_lookup.get_template('about.html')
        html_content = mako_template.render()
        return html_content

    @cherrypy.expose
    def all_special_offers(self):
        mako_template = mako_lookup.get_template('all_special_offers.html')
        html_content = mako_template.render()
        return html_content

    @cherrypy.expose
    def test(self, name):
        mako_template = mako_lookup.get_template('test.html')
        html_content = mako_template.render(name=name)
        return html_content

    @cherrypy.expose
    @log_request
    @cherrypy.tools.json_out()
    def render_avatar(self):
        valid_email = cherrypy.session.get("authenticated_email", None)
        valid_legalname = cherrypy.session.get("authenticated_legalname",
                                               "未登录用户")
        valid_photo = cherrypy.session.get("authenticated_photo", None)
        user_info = {
            "username": valid_legalname,
            "email": valid_email,
            "avatar_photo": valid_photo
        }
        return json.dumps(user_info)

    @cherrypy.expose
    def shutdown(self):
        server_base.kill_child_threads()
        cherrypy.engine.exit()
        return "Successful"


cherrypy.quickstart(MDRT(), '', cherrypy_conf)

my_logger.info(f"{__name__} 运行到尾部。")
