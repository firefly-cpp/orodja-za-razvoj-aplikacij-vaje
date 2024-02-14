import web
import json
import psycopg2

con = psycopg2.connect(user="uporabnik",
                       password="uporabnikuporabnikuporabnik",
                       host="127.0.0.1",
                       port="5432",
                       database="triatlon")

urls = (
    '/api/tekmovalec/(.+)', 'Tekmovalec',
    '/api/tekmovalci/', 'Tekmovalci'
)

app = web.application(urls, globals())


class Tekmovalec:
    def GET(self, t_id):
        t_id = format(t_id)
        web.header('Content-Type', 'application/json')
        web.header('Access-Control-Allow-Origin', '*')

        with con:
            cur = con.cursor()
            cur.execute(
                "SELECT * FROM rezultat2 WHERE ID=%(id)s", {'id': t_id})

            while True:
                row = cur.fetchone()

                if row is None:
                    a = {'skupni_cas': 'empty'}
                    odgovor = json.dumps(a)
                    return (odgovor)
                a = {'skupni_cas': row[17]}
                odgovor = json.dumps(a)
                return (odgovor)


class Tekmovalci:
    def GET(self):
        web.header('Content-Type', 'application/json')
        web.header('Access-Control-Allow-Origin', '*')

        with con:
            cur = con.cursor()
            cur.execute(
                "SELECT ID, cas_plavanja, cas_kolesarjenja, cas_teka, skupni_cas FROM rezultat2 LIMIT 2000")

            while True:
                glava = (
                    'ID',
                    'cas_plavanja',
                    'cas_kolesarjenja',
                    'cas_teka',
                    'skupni_cas')

                rezultati = []
                for vrstica in cur.fetchall():
                    rezultati.append(dict(zip(glava, vrstica)))
                break

        return (json.dumps(rezultati, indent=2))


if __name__ == "__main__":
    app.run()
