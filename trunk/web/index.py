#!/usr/bin/env python

import sys
import web

from queriesdb import QueriesDB
from tests import db_config
from tests import report_data, map_data, tags
from tests import user

sys.path.append('/home/mapastematicos/pylibs/')
render = web.template.render('templates/')

urls = (
        '/', 'Index',
        '/map/(.+)', 'Map',
        '/tag/(.+)', 'Tag',
        '/search', 'Search'
)

app = web.application(urls, globals())

class Index:
    def GET(self):
        name = ""
        return render.index(name)


class Map:
    def GET(self, id_map):
        q = QueriesDB(db_config)
        #tagnames = q.getTags(id_map)
        tagnames = {'1': 't1', '2': 't2', '3': 't3'}
        title    = q.getTitle(id_map)
        vars = [tagnames, title]
        if title == None:
            msg = "Lo sentimos, pero parece que no tenemos el mapa que nos pide."
            return render.notfound(msg)
        return render.map(vars)


class Tag:
    def GET(self, id_tag):
        #q = QueriesDB(db_config)
        #resultset = q.getResultsByTag(id_tag)
        resultset = {'12345678901234567890123456789012': 'titulo 1 del mapa',
                     '12345678901234567890123456789012': 'titulo 2 del mapa',
                     '12345678901234567890123456789012': 'titulo 3 del mapa'
                     }
        if resultset == None:
            msg = "Lo sentimos, pero parece que no tenemos la etiqueta que nos pide."
            return render.notfound(msg)
        return render.search(resultset)


class Search:
    def GET(self):
        resultset = {"1": "oe",
                     "2": "eo"}
        if resultset == None:
            msg = "Lo sentimos, pero parece que no hemos encontrado nada como lo que nos pide."
            return render.notfound(msg)
        return render.search(resultset)



if __name__ == "__main__":
    app.run() #this is normally only called from dispatch.cgi

else:
    web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
