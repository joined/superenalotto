# -*- coding: UTF-8 -*- #
from flask import Flask, render_template
import requests
import lxml.html

superEnalotto = Flask(__name__)

plays = [[7,  16, 22, 56, 67, 88],
         [9,  14, 36, 56, 67, 87],
         [8,  31, 35, 45, 66, 87],
         [10, 21, 30, 57, 63, 74],
         [13, 40, 56, 74, 81, 90],
         [16, 23, 40, 55, 60, 82],
         [16, 41, 43, 52, 61, 80],
         [3,  27, 33, 36, 57, 84]]


def get_estrazioni():
    r = requests.get("http://www.superenalotto.com/archivio-estrazioni.asp")

    lxml_root = lxml.html.fromstring(r.text)

    # Get all rows of the table with extractions, identified
    # by class "t1"
    rows = lxml_root.xpath("//table[@class='t1']/tbody/tr")

    extractions = []

    for row in rows:
        # Get extraction date from "th" element
        date = row.xpath("th")[0].text_content().strip()

        # Get numbers of the extraction
        extraction_numbers = [int(td.text_content().strip())
                              for td
                              in row.xpath("td//td[position() <= 6]")]

        combinations = []

        for play in plays:
            combination = []

            for number in play:
                match = True if number in extraction_numbers else False

                combination.append({'value': number, 'match': match})

            combinations.append(combination)

        extractions.append({'date': date, 'combinations': combinations})

    return extractions


@superEnalotto.route('/')
def index():
    extractions = get_estrazioni()

    return render_template('index.html', extractions=extractions)
