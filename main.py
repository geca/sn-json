#!/usr/bin/env python
import os
import jinja2
import webapp2
import json
import datetime

from google.appengine.api import urlfetch


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        osebe_besedilo = open("people.json", "r").read()
        osebe = json.loads(osebe_besedilo)

        return self.render_template("hello.html", {"osebe": osebe})

class VremeHandler(BaseHandler):
    def get(self):

        naslov_napovedi = "http://api.openweathermap.org/data/2.5/weather?q=Maribor,si&units=metric&appid=1afb80eedc28c08ad55176ae3b63d462"
        rezultat_zahteve = urlfetch.fetch(naslov_napovedi)
        surovi_json = rezultat_zahteve.content
        vreme = json.loads(surovi_json) # Python slovar

        surovi_soncni_vzhod = vreme["sys"]["sunrise"]

        soncni_vzhod = datetime.datetime.fromtimestamp(
            surovi_soncni_vzhod
        ).strftime('%d.%m.%Y %H:%M:%S')

        vreme["sv"] = soncni_vzhod


        return self.render_template("vreme.html", vreme)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/vreme', VremeHandler)
], debug=True)
