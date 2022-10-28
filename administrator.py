#!/usr/bin/env python3

from my_utility_scripts.logging_tools import log_request, my_logger

my_logger.info(f"开始运行module:{__name__}, 其文件位置在: {__file__}")

import os
import pickle
import json
import cherrypy

from my_mako_adaptor import mako_lookup
import server_base
import articles_storage


class UnitServer(server_base.BasicServer):

    mako_template_for_server_index = "administrator.html"
    SCRIPT_NAME = "administrator"

    @cherrypy.expose
    def get_existing_articles_structure(self):
        return json.dumps(articles_storage.articles_structure_map)

    @cherrypy.expose
    def uploading_article(self, node_path, article_title, article_excerpt,
                          article_body):
        node_path = node_path.split(',')
        my_logger.info(f"""<uploading_article>收到的参数是：
        node_path: {node_path}
        article_title: {article_title}
        article_excerpt: {article_excerpt}
        article_body: {article_body}""")
        article_identifer = article_title.strip()
        if node_path[0] == "our_perspectives":
            article_group = "perspectives"
            article_body = """
                            <%inherit file="perspective_template.mako"/>
                            """ + article_body
        else:
            article_group = "special_offers"
            article_body = """
                            <%inherit file="basepage.mako"/>

                            <%block name="html_head">
                              ${parent.html_head()}
                              <link rel="stylesheet" type="text/css" href="/static/all_special_offers.css">
                            </%block>
                            """ + article_body
        new_article_url = os.path.join("static", article_group,
                                       article_identifer)
        with open(new_article_url, "w") as article_file:
            article_file.write(article_body)
        article_metadata = {
            "article_title": article_title,
            "article_excerpt": article_excerpt
        }
        articles_storage.append_node(node_path.pop(),
                                     (article_identifer, article_metadata))
        return f"Successfully uploaded file: {article_title}"

    @cherrypy.expose
    def uploading_image(self, file):
        my_logger.info(f"<uploading_image>收到的参数是: file: {file}")
        storage_path = "static/article_images"
        storage_url = os.path.join(storage_path, file.filename)
        my_logger.info(f"<uploading_image>准备存储的路径是: {storage_url}")
        with open(storage_url, "wb") as f:
            f.write(file.file.read())
        return json.dumps({"location": "/" + storage_url})

    @cherrypy.expose
    def delete_an_article(self, deleting_entry_indentifier):
        """
        # remove file:
        try:
            target_url = f"static/perspectives/{deleting_entry_indentifier}"
            assert os.path.isfile(target_url)
            os.remove(target_url)
        except Exception as e:
            my_logger.warning(f"在试图删除文件<{file_identifier}>的过程中出现错误：{e}")
        # remove structure_map:
        old_articles_list = articles_storage.articles_structure_map[
            article_info['article_group']][article_info["article_category"]][
                article_info["article_subcategory"]]
        new_articles_list = [
            x for x in old_articles_list
            if x["article_identifer"] != article_info['article_identifer']
        ]
        articles_storage.articles_structure_map[article_info['article_group']][
            article_info["article_category"]][
                article_info["article_subcategory"]] = new_articles_list
        self._update_pickled_map()
        """
        articles_storage.delete_an_article(deleting_entry_indentifier)
        return f"Successfully deleted file {deleting_entry_indentifier}"

    def _update_pickled_map(self):
        with open(self.articles_map_pickle, "wb") as output_file:
            pickle.dump(articles_storage.articles_structure_map, output_file)
