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
    Richiede la lista delle estrazioni degli ultimi 90 giorni
    dal sito ufficiale del SuperEnalotto, fa un parsing della pagina e
    restituisce la lista con le estrazioni nel formato
    [
        {'data': 'GG MMM YYYY', 'numeri': [1,2,3,4,5,6]},
        {'data': 'GG MMM YYYY', 'numeri': [1,2,3,4,5,6]},
        ...
    ]
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
        numeri = [td.text_content().strip()
                  for td
                  in riga.xpath("td/table/tbody/tr/td")]

        # Tengo solo i primi 6 numeri, gli altri non mi interessano
        estrazioni.append({'data': data, 'numeri': numeri[:6]})

    return estrazioni


def check_estrazione(numeri_estrazione):
    """
    Data un'estrazione, ovvero una lista con i numeri dell'estrazione,
    restituisce una lista con i numeri vincenti per ogni giocata,
    nel formato
    [
        [1, 2],
        [3, 4],
        [5, 6]
    ]
    """

    risultato = []

    for giocata in giocate:
        # Tengo i numeri dell'estrazione che sono presenti nella giocata
        # corrente
        numeri_giusti = [num for num
                         in numeri_estrazione
                         if int(num) in giocata]

        # Se almeno un numero della giocata corrente è giusto,
        # aggiungilo alla lista dei risultati
        if len(numeri_giusti) > 0:
            risultato.append(numeri_giusti)

    return risultato


@superEnalotto.template_filter('pluralizza')
def pluralizza(numero, singolare='o', plurale='i'):
    """
    Filtro per gestire il plurale
    """

    return singolare if numero == 1 else plurale


@superEnalotto.route('/')
def index():
    """
    La principale ed unica route. Prende le estrazioni dal sito ufficiale,
    poi fa la verifica delle giocate vincenti e risponde con il template 
    compilato con le estrazioni
    """

    estrazioni = get_estrazioni()

    for estrazione in estrazioni:
        # Aggiungo all'estrazione corrente un campo con i numeri vincenti
        estrazione['combinazioni'] = check_estrazione(estrazione['numeri'])

    return render_template('index.html', estrazioni=estrazioni)
