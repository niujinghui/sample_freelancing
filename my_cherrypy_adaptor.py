#!/usr/bin/env python3

import os

ROOT_ABSOLUTE_PATH = os.path.abspath(os.path.dirname(__file__))

cherrypy_conf = {
    "global": {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 80
    },
    "/": {
        "tools.sessions.on": True,
        'tools.encode.on': True,
        'tools.encode.encoding': "utf-8",
        'tools.expires.on': True,
        'tools.expires.secs': 0,
        'tools.expires.force': True,
        "tools.staticdir.root": ROOT_ABSOLUTE_PATH
    },
    "/gui_images": {
        "tools.staticdir.on": True,
        "tools.staticdir.dir": "static/gui_images"
    },
    "/static": {
        "tools.staticdir.on": True,
        "tools.staticdir.dir": "static"
    },
    "/favicon.ico": {
        "tools.staticfile.on": True,
        "tools.staticfile.filename": os.path.abspath("static/gui_images/favicon.jpg")
    }
}
