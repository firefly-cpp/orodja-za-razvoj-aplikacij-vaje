import os
import csv
import datetime
import psycopg2


class Tekmovanje(object):
    def __init__(self, ime_tekmovanja, leto_izvedbe, rezultati):
        self.ime_tekmovanja = ime_tekmovanja
        self.leto_izvedbe = leto_izvedbe
        self.rezultati = rezultati


class Rezultat(object):
    def __init__(
            self,
            ime_tekmovalca,
            uvrstitev_spol,
            uvrstitev_kategorija,
            uvrstitev_skupna,
            bib,
            kategorija,
            starost,
            kraj,
            drzava,
            poklic,
            tocke,
            cas_plavanja,
            cas_t1,
            cas_kolesarjenja,
            cas_t2,
            cas_teka,
            skupni_cas):
        self.ime_tekmovalca = ime_tekmovalca
        self.uvrstitev_spol = uvrstitev_spol
        self.uvrstitev_kategorija = uvrstitev_kategorija
        self.uvrstitev_skupna = uvrstitev_skupna
        self.bib = bib
        self.kategorija = kategorija
        self.starost = starost
        self.kraj = kraj
        self.drzava = drzava
        self.poklic = poklic
        self.tocke = tocke
        self.cas_plavanja = cas_plavanja
        self.cas_t1 = cas_t1
        self.cas_kolesarjenja = cas_kolesarjenja
        self.cas_t2 = cas_t2
        self.cas_teka = cas_teka
        self.skupni_cas = skupni_cas


pot_do_datotek = "/home/user/IRONMAN/CSV"
datoteke = os.listdir(pot_do_datotek)
datoteke_csv = list(filter(lambda f: f.endswith('.csv'), datoteke))

vsi_rezultati = []


def if_missing(podatek):
    if podatek == "---":
        return ("EMPTY")
    elif len(podatek) == 0:
        return ("EMPTY")
    else:
        return (podatek)


def get_kraj_izvedba(podatek):
    podatki = podatek.split("_")
    return (podatki[1], podatki[2].strip(".csv"))


zacetek = datetime.datetime.now()
for i in range(len(datoteke_csv)):
    rezultati = []
    kraj, izvedba = get_kraj_izvedba(datoteke_csv[i])
    with open(pot_do_datotek + "/" + datoteke_csv[i], 'r', encoding='utf-8') as file:
        datoteka = csv.DictReader(file)
        for vrstica in datoteka:
            rezultati.append(
                Rezultat(
                    if_missing(
                        vrstica['name']), if_missing(
                        vrstica['genderRank']), if_missing(
                        vrstica['divRank']), if_missing(
                        vrstica['overallRank']), if_missing(
                            vrstica['bib']), if_missing(
                                vrstica['division']), if_missing(
                                    vrstica['age']), if_missing(
                                        vrstica['state']), if_missing(
                                            vrstica['country']), if_missing(
                                                vrstica['profession']), if_missing(
                                                    vrstica['points']), if_missing(
                                                        vrstica['swim']), if_missing(
                                                            vrstica['t1']), if_missing(
                                                                vrstica['bike']), if_missing(
                                                                    vrstica['t2']), if_missing(
                                                                        vrstica['run']), if_missing(
                                                                            vrstica['overall'])))
    vsi_rezultati.append(Tekmovanje(kraj, izvedba, rezultati))
konec = datetime.datetime.now()

print("Vseh datotek: ", len(vsi_rezultati))
stevec_rez = 0
for i in range(len(vsi_rezultati)):
    current = vsi_rezultati[i].rezultati
    stevec_rez = stevec_rez + len(current)
print('Vseh rezultatov: ', stevec_rez)
trajanje = konec - zacetek
trajanje_s = trajanje.total_seconds()
print("Cas razclenjevanja: ", trajanje_s, " sekund")

# vpis v bazo
try:
    connection = psycopg2.connect(user="uporabnik",
                                  password="uporabnikuporabnikuporabnik",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="triatlon")
    cursor = connection.cursor()

    postgres_insert_query = """ INSERT INTO rezultat2 (ime_tekmovalca, uvrstitev_spol, uvrstitev_kategorija, uvrstitev_skupna, bib, kategorija, starost, kraj, drzava, poklic, tocke, cas_plavanja, cas_t1, cas_kolesarjenja, cas_t2, cas_teka, skupni_cas) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

    for i in range(len(vsi_rezultati)):  # skozi vsa tekmovanja
        for j in range(
                len(vsi_rezultati[i].rezultati)):  # skozi vse rezultate tekmovanja
            print(vsi_rezultati[i].rezultati[j].ime_tekmovalca)
            vpis = (
                vsi_rezultati[i].rezultati[j].ime_tekmovalca,
                vsi_rezultati[i].rezultati[j].uvrstitev_spol,
                vsi_rezultati[i].rezultati[j].uvrstitev_kategorija,
                vsi_rezultati[i].rezultati[j].uvrstitev_skupna,
                vsi_rezultati[i].rezultati[j].bib,
                vsi_rezultati[i].rezultati[j].kategorija,
                vsi_rezultati[i].rezultati[j].starost,
                vsi_rezultati[i].rezultati[j].kraj,
                vsi_rezultati[i].rezultati[j].drzava,
                vsi_rezultati[i].rezultati[j].poklic,
                vsi_rezultati[i].rezultati[j].tocke,
                vsi_rezultati[i].rezultati[j].cas_plavanja,
                vsi_rezultati[i].rezultati[j].cas_t1,
                vsi_rezultati[i].rezultati[j].cas_kolesarjenja,
                vsi_rezultati[i].rezultati[j].cas_t2,
                vsi_rezultati[i].rezultati[j].cas_teka,
                vsi_rezultati[i].rezultati[j].skupni_cas)
            print(vpis)
            cursor.execute(postgres_insert_query, vpis)
            print("Zapis v bazo vnesen.")

    connection.commit()
    count = cursor.rowcount
    print(count, "Uspesno vneseno.")

except (Exception, psycopg2.Error) as error:
    if(connection):
        print("Napaka", error)
finally:
    if(connection):
        cursor.close()
        connection.close()
        print("Povezava z bazo prekinjena.")
