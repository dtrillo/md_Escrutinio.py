__author__ = 'dtrillo'

import time, urllib2
from cookielib import CookieJar
from urllib2 import urlopen
from bs4 import BeautifulSoup as bs

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
nl = "\n"
version = "0.5.2"
miVersion = "Escrutinio - version", version, " http://www.manejandodatos.es"

# Listado de Funciones
def saveFile(file, data):
    sfile = open(file,"w")
    sfile.write(data)
    sfile.close()

def saveList2File(file, lista, mostrar=False):
    """ Graba una lista a un fichero de texto
            Incluso puede mostrar el resultado en pantalla    """
    sfile = open(file,"w")
    for linea in lista:
        sfile.writelines(str(linea) + nl)
        if mostrar: print str(linea)
    sfile.close()

def gethtml(url, fichHTML):
    """ Recupera codigo HTML a partir de URL """
    try:
        texto = opener.open (url).read()
        saveFile(fichHTML, texto) # Grabo fichero
        return texto
    except Exception, e:
        print "Error: ", str(e)
        time.sleep(2)
        return ''

def EsLineaValida(linea):
    if len(linea) == 0: return False
    if "*" in linea: return False
    if "Euros" in linea: return False
    return True

def Escrutinio(data, ficheroSalida):
    soup = bs(data)

    # Busco la Recaudacion
    tEscritunio = soup.findAll("table", { "class" : "fill-table m1015" }) # TABLA

    tr = []
    for mydiv in tEscritunio:
        rows = mydiv.findAll('tr')
        for row in rows:
            if EsLineaValida(row.text):
                tmp = row.text.strip().split(nl)[-1] # SOLO me interesa la ULTIMA COLUMNA
                tr.append(tmp.replace('.','')) # Ajuste de . de miles

    # Guardo la INFO en un fichero de TEXTO, q sera usado por SEF
    print len(tr)
    if len(tr) == 8:
        saveList2File(ficheroSalida, tr, True)
        print "Escrutinio recuperada!"
    else:
        print tr
        #saveList2File(ficheroSalida,tr)
        print "DATOS de Escrutinio NO son  los esperados!"
    time.sleep(2)

# Valores
ficheroEscrutinioHTML = 'recaudacion.html'
ficheroEscrutinio = 'recaudacion.txt'
urlEscrutinio = 'http://1x2.marca.com'

if __name__ == '__main__':
    print miVersion
    data =  gethtml(urlEscrutinio, ficheroEscrutinioHTML)
    Escrutinio(data, ficheroEscrutinio)
