#!/usr/bin/env python

import sys
sys.path.append('/home/mapastematicos/pylibs/')
import web

from queriesdb import QueriesDB
from tests import db_config
from tests import report_data, map_data, tags
from tests import user

render = web.template.render('templates/')

urls = ('/', "Beta",
        '/index', 'Index',
        '/map/(.+)', 'Map',
        '/tag/(.+)', 'Tag',
        '/search', 'Search',
        '/thanks', 'Thanks',
        '/about', 'About'
)

app = web.application(urls, globals())

class Beta:
    def GET(self):
        return render.beta()
    
class Index:
    def GET(self):
        q = QueriesDB(db_config)
        resultset = q.getMoreViewedTags()
        return render.index(resultset)

class Thanks:
    def GET(self):
        return render.gracias()

class About:
    def GET(self):
        return render.about()


class Map:
    def GET(self, id_map):
        q = QueriesDB(db_config)
        tagnames = q.getTags(id_map)
        title    = q.getTitle(id_map)
        vars     = [tagnames, title]

        if (title == None) and (tagnames == None):
            msg = "Lo sentimos, pero parece que no tenemos el mapa que nos pide."
            return render.notfound(msg)
        else:
            title = ""
            tagnames = {"None":"None"}
            return render.map(vars, id_map + ".png", id_map + "_stats.png")


class Tag:
    def GET(self, id_tag):
        q = QueriesDB(db_config)
        resultset = q.getResultsByTag(id_tag)
        if resultset == None:
            msg = "Lo sentimos, pero parece que no tenemos mapas con la etiqueta que nos pide."
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
