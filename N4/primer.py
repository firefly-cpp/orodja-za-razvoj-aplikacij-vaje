import web # vkljucimo knjiznico web.py
import requests # za klicanje spletnih storitev
from json2html import * # za pretvorbo json v html

urls = ( # navigacija
    "/domov", "domov",
    "/rezultati", "rezultati")

app = web.application(urls, globals())

class domov: # razred domov
    def GET(self):
        return 'Pozdravljeni!'

class rezultati: # razred za pridobivanje podatkov
    def GET(self):
        response = requests.get("http://0.0.0.0:8080/api/tekmovalci/")
        odgovor = response.status_code
        if odgovor == 200:
            rezultat = json2html.convert(json = response.json())
        else:
            rezultat = 'Napaka'
        return rezultat

if __name__ == "__main__": #zagon programa
    app.run()
