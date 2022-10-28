#!/usr/bin/env python3

from my_utility_scripts.logging_tools import log_request, my_logger

my_logger.info(f"开始运行module:{__name__}, 其文件位置在: {__file__}")

import os
import pickle
import pprint

ARTICLES_MAP_PICKLE_URL = "articles_structure_map.pickle"
ARTICLES_STORAGE_DIRECTORIES = ["perspectives", "special_offers"]

assert os.path.getsize(ARTICLES_MAP_PICKLE_URL) > 0
with open(ARTICLES_MAP_PICKLE_URL, "rb") as inpt_file:
    articles_structure_map = pickle.load(inpt_file)


def _update_pickled_map():
    with open(ARTICLES_MAP_PICKLE_URL, "wb") as output_file:
        pickle.dump(articles_structure_map, output_file)


def get_node(node_identifer, starting_root=articles_structure_map):
    my_logger.info(f"进入{starting_root[0]}")
    found_node = None
    if starting_root[0] == node_identifer:
        found_node = starting_root
        return found_node
    else:
        if isinstance(starting_root[1], list):
            for subnode in starting_root[1]:
                found_node = get_node(node_identifer=node_identifer,
                                      starting_root=subnode)
                if found_node:
                    return found_node


def append_node(parent_node_identifier, new_node):
    parent_node = get_node(parent_node_identifier)
    parent_node[1].append(new_node)
    _update_pickled_map()


class NodeTraversal:
    def _get_path(self, head_node):
        if head_node[0] == self.target_node_name:
            self.path_stack.append(head_node)
            return True
        if isinstance(head_node[1], list):
            for subnode in head_node[1]:
                if self._get_path(subnode):
                    self.path_stack.append(head_node)
                    return True
        return False

    def get_path(self, node_name, head_node=articles_structure_map):
        self.path_stack = []
        self.target_node_name = node_name
        self._get_path(head_node)
        return list(reversed(self.path_stack))


def delete_an_article(article_identifier):
    # delete file:
    for d in ARTICLES_STORAGE_DIRECTORIES:
        url_path = os.path.abspath(f'static/{d}')
        if article_identifier in os.listdir(url_path):
            my_logger.warning(
                f"Deleting file <{article_identifier}> in directory {d}")
            os.remove(os.path.join(url_path, article_identifier))
    # delete the corresponding node:
    nt = NodeTraversal()
    path = nt.get_path(article_identifier)
    old_articles_list = path[-2][1]
    target_article_node = get_node(article_identifier)
    old_articles_list.remove(target_article_node)
    _update_pickled_map()


def pprint_entire_map():
    pprint.pprint(articles_structure_map)
