import web  # vkljucimo knjiznico web.py
import requests  # za klicanje spletnih storitev
from json2html import *  # za pretvorbo json v html

# navigacija
urls = (
    "/domov", "domov",
    "/rezultati", "rezultati")

app = web.application(urls, globals())


# razred domov
class domov:
    def GET(self):
        return 'Pozdravljeni!'


# razred za pridobivanje podatkov
class rezultati:
    def GET(self):
        response = requests.get("http://0.0.0.0:8081/api/tekmovalci/")
        odgovor = response.status_code
        if odgovor == 200:
            rezultat = json2html.convert(json=response.json())
        else:
            rezultat = 'Napaka'
        return rezultat


# zagon programa
if __name__ == "__main__":
    app.run()
