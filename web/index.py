#!/usr/bin/env python

import sys
sys.path.append('/home/mapastematicos/pylibs/')

import web
render = web.template.render('templates/')

urls = (
    "/(.*)", "Hello"
)

app = web.application(urls, globals())

class Hello:
    def GET(self, name):
        return render.index(name)


if __name__ == "__main__":
    app.run() #this is normally only called from dispatch.cgi

else:
    web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
