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
    r = requests.get("http://www.superenalotto.com/archivio-estrazioni.asp")

    lxml_root = lxml.html.fromstring(r.text)
    righe = lxml_root.xpath("//table[@class='t1']/tbody/tr")

    estrazioni = []

    for riga in righe:
        data = riga.xpath("th")[0].text_content().strip()

        numeri = [td.text_content().strip()
                  for td
                  in riga.xpath("td/table/tbody/tr/td")]

        estrazioni.append({'data': data, 'numeri': numeri[:6]})

    return estrazioni


def check_giocate(numeri_estrazione):
    risultato = []

    for giocata in giocate:
        numeri_giusti = [num for num
                         in numeri_estrazione
                         if int(num) in giocata]

        if len(numeri_giusti) > 0:
            risultato.append(numeri_giusti)

    return risultato


@superEnalotto.template_filter('lunghezza_testuale')
def lunghezza_testuale(mylist):
    if len(mylist) == 1:
        return '1 numero'
    else:
        return str(len(mylist)) + ' numeri'


@superEnalotto.route('/')
def index():
    est = get_estrazioni()

    for e in est:
        e['combinazioni'] = check_giocate(e['numeri'])

    return render_template('index.html', estrazioni=est)
