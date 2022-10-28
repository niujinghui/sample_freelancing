#!/usr/bin/env python3

import ast
from pprint import pprint
from .logging_tools import my_logger, stringify_attrs


class AST_Analyzer(ast.NodeVisitor):
    def __init__(self, classname=None):
        self.looking_for_classname = classname
        self.classes_found = []

    def visit_ClassDef(self, node):
        # pprint(stringify_attrs(node))
        if self.looking_for_classname:
            if node.name == self.looking_for_classname:
                self.classes_found.append(node)
            return
        self.classes_found.append(node)
        # self.generic_visit(node)

    """
    def visit_Assign(self, node):
        global counter
        counter["visit_Assign"] += 1
        print("entering <visit_Assign>")
        pprint(stringify_attrs(node))
        # import pdb
        # pdb.set_trace()
        if len(node.targets) == 1:
            if self.looking_for_classAttr:
                if self.looking_for_classAttr == node.targets[0].id:
                    self.assignments_found.append(node)
            return
        self.assignments_found.append(node)
        # self.generic_visit(node)
    """

    def report(self):
        pprint(self.classes_found)


def extract_ClassDefs(source_file_content, classname=None, hasClassAttr=None):
    target_found = None  # 默认是没有发现任何目标
    # 开始分析：
    ast_analyzer = AST_Analyzer(classname=classname)
    ast_tree = ast.parse(source_file_content)
    ast_analyzer.visit(ast_tree)
    if len(ast_analyzer.classes_found) == 1:
        target_class = ast_analyzer.classes_found[0]
        for gut in target_class.body:
            if not isinstance(gut, ast.Assign):
                continue
            if not isinstance(gut.targets[0], ast.Name):
                continue
            if gut.targets[0].id == hasClassAttr:
                target_found = {"SCRIPT_NAME": gut.value.s}
    return target_found


"""
f = open('auth.py', 'r')
content = f.read()
result = extract_ClassDefs(content,
                           classname='UnitServer',
                           hasClassAttr="SCRIPT_NAME")
pprint(result)
"""