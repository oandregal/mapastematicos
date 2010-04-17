#!/usr/bin/env python

import sys
import web

sys.path.append('/home/mapastematicos/pylibs/')
render = web.template.render('templates/')

urls = (
    "/", "Index",
    "/map", "Map",
    "/search", "Search"
)

app = web.application(urls, globals())

class Map():
    def GET(self):
        name="foo"
        return render.map(name)


class Index:
    def GET(self):
        return render.index()


class Search:
    def GET(self):
        return render.search()

if __name__ == "__main__":
    app.run() #this is normally only called from dispatch.cgi

else:
    web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
