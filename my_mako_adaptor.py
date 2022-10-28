import mako.lookup
import os
import cherrypy

static_directory = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                "static")
offers_directory = os.path.join(static_directory, "special_offers")
perspectives_directory = os.path.join(static_directory, "perspectives")
cherrypy.log("<static_directory> 是: {}".format(static_directory))
compiled_templates_directory = os.path.join(static_directory,
                                            "compiled_templates")
cherrypy.log("<compiled_templates_directory> 是: {}".format(
    compiled_templates_directory))

mako_lookup = mako.lookup.TemplateLookup(
    directories=[static_directory, offers_directory, perspectives_directory],
    input_encoding="utf-8",
    output_encoding='utf-8',
    module_directory=compiled_templates_directory)
