# -*- coding: UTF-8 -*- #
from flask import Flask, render_template
import requests
import lxml.html

superEnalotto = Flask(__name__)

giocate = [[7, 16, 22, 56, 67, 88],
           [9, 14, 36, 56, 67, 87],
           [8, 31, 35, 45, 66, 87],
           [10, 21, 30, 57, 63, 74],
           [13, 40, 56, 74, 81, 90],
           [16, 23, 40, 55, 60, 82],
           [16, 41, 43, 52, 61, 80],
           [3, 27, 33, 36, 57, 84]]


def get_estrazioni():
    """
    Questa funzione fa schifo.
    Non fate mai niente di simile, vi prego.
    """

    r = requests.get("http://www.superenalotto.com/archivio-estrazioni.asp")

    lxml_root = lxml.html.fromstring(r.text)

    # Cerco tutte le righe della tabella con le estrazioni,
    # identificata dalla classe "t1"
    righe = lxml_root.xpath("//table[@class='t1']/tbody/tr")

    estrazioni = []

    for riga in righe:
        # Prendo la data dall'elemento "th" della riga
        data = riga.xpath("th")[0].text_content().strip()

        # Prendo i numeri dell'estrazione come celle della
        # sotto-tabella
        numeri_estrazione = [int(td.text_content().strip())
                             for td
                             in riga.xpath("td/table/tbody/tr/td")]

        combinazioni = []

        for giocata in giocate:
            combinazione = []

            for numero in giocata:
                preso = True if numero in numeri_estrazione[:6] else False

                combinazione.append({'numero': numero, 'preso': preso})

            combinazioni.append(combinazione)

        estrazioni.append({'data': data, 'combinazioni': combinazioni})

    return estrazioni


@superEnalotto.route('/')
def index():
    """
    La principale ed unica route. Prende le estrazioni dal sito ufficiale,
    poi fa la verifica delle giocate vincenti e risponde con il template
    compilato con le estrazioni
    """

    estrazioni = get_estrazioni()

    return render_template('index.html', estrazioni=estrazioni)
