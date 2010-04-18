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
        '/tag', 'Tag',
        '/search', 'Search'
)

app = web.application(urls, globals())

class Index:
    def GET(self):
        return render.index()


class Map:
    def GET(self, id_map):
        q = QueriesDB(db_config)
        tagnames = q.getTags(id_map)
        return render.map(tagnames)


class Tag:
    def GET(self):
        return render.search()


class Search:
    def GET(self):
        return render.search()



if __name__ == "__main__":
    app.run() #this is normally only called from dispatch.cgi

else:
    web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)