# coding: utf-8
#-------------------------------------------------------------------------------
# Name:        ExtraeMarcadores
# Purpose:      Extrae marcadores de 1D o 2D de la Liga de Futbol Española
#
# Author:      david - http://www.manejandodatos.es
#
# Created:     24/01/2014
# Copyright:   (c) david 2014
# Licence:
#-------------------------------------------------------------------------------
import sys, urllib2, time
from cookielib import CookieJar
from bs4 import BeautifulSoup as bs
import unicodedata # Tildes http://www.leccionespracticas.com/uncategorized/eliminar-tildes-con-python-solucionado/

miVersion = "Resultados de partidos - www.manejandodatos.es - Versión 0.6.0"
# Elimina TILDES
def elimina_tildes(s): return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))


urlMarca = ["http://www.marca.com/futbol/primera/calendario.html", "http://www.marca.com/futbol/segunda/calendario.html"]
separaGoles = "-"

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

class Marcadores():
    """ Datos extraidos desde MARCA.com con los marcadores """
    def __init__(self, eql, eqv, golL, golV ):
        self.eql = eql.lower().decode('utf-8')
        self.eqv =  eqv.lower().decode('utf-8')
        self.golL = golL
        self.golV = golV
    def __str__(self):
        return self.eql + " " + self.eqv + " --> " + self.golL + " - " + self.golV

def gethtml(url):
    """ Recupera codigo HTML a partir de URL """
    try:
        texto = opener.open (url).read()
        return texto
    except Exception, e:
        print "Error: ", str(e)
        time.sleep(2)
        return ''


def pregunta(mensaje, opciones):
    """ Recupera un valor preguntando al usuario """
    ask = raw_input(mensaje)
    try:
        return int(ask) if int(ask) in opciones else ''
    except:
        return ''

def obtenerResultados(data, jorn):
    """ Ejecuta la extracción de la información desde el código HTML extraido """
    soup = bs(data)
    tjornadas = soup.findAll("div", { "class" : "jornada calendarioInternacional" })
    print len(tjornadas), " jornadas"
    #for jornada in tjornadas:
    #    print jornada.text
    #print tjornadas[jorn-1]
    tlocales = tjornadas[jorn-1].findAll("td", { "class" : "local" })
    tvisits = tjornadas[jorn-1].findAll("td", { "class" : "visitante" })
    tresults = tjornadas[jorn-1].findAll("td", { "class" : "resultado" })
    #print len(tlocales), len(tvisits), len(tresults)
    lMarcadores = []
    for i in range(0,len(tlocales)):
        goles = tresults[i].text.split(separaGoles)
        goles = ajustaGoles(goles)
        partido = Marcadores(elimina_tildes(tlocales[i].text), elimina_tildes(tvisits[i].text), goles[0], goles[1])
        lMarcadores.append(partido)
    return lMarcadores   # tjornadas[jorn-1].text


def ajustaGoles(marca):
    """ Ajuste de goles, devolviendo gol como string """
    try:
        marca[0] = str(int(marca[0]))
        marca[1] = str(int(marca[1]))
    except:
        marca[0] = ''
        marca[1] = ''
    return marca

def main():
    div = pregunta('Primera o segunda division: 1 o 2', [1,2])
    if div == 0:
        print "Error all seleccionar division!"
        sys.exit()
    jornada = pregunta('Numero de jornada: ', range(1,43))
    if jornada == 0:
        print "Error all seleccionar division!"
        sys.exit()

    #print urlMarca[div - 1], jornada
    data = gethtml(urlMarca[div - 1])
    marcadores = obtenerResultados( data, jornada)
    for marc in marcadores:
        print marc

if __name__ == '__main__':
    print miVersion
    main()
