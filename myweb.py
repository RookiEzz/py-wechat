# -*- encoding:UTF-8 -*-
import web
render = web.template.render("templates")
urls = (
    '/index','index',
    '/blog/\d+','Blog',
    '/(.*)', 'hello'
)
app = web.application(urls, globals())

class hello:
    def GET(self,qrSource):
        print
        return render.hello(qrSource)
class index:
    def GET(self):
        return web.input()
class Blog:
    def POST(self):
        return web.input()
    def GET(self):
        return web.ctx.env
app.run()