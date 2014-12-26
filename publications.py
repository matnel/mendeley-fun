# -*- coding: utf-8 -*-

def to_string( publication ):

    text = ''

    ## authors

    authors = []

    for author in publication['authors']:
        a = author['surname'].encode('utf8') + ' ' + author['forename'][0].encode('utf8') + '.'

        if author['surname'] == 'Nelimarkka':
            a = '**' + a + '**'

        authors.append( a )

    text += ', '.join( authors )

    ## year
    text += ' (' + str(publication['year']) + '): '

    ## title
    text += publication['title'].encode('utf8') + '.'

    if publication['venue']:
        text += ' ' + publication['venue'].encode('utf8')

    return text

from common import *

import json

session = mendeley()

mine = []

everything = session.documents.iter( page_size = 500, view = 'all' )

for publication in everything:

    if publication.authored and not publication.hidden:
        mine.append( publication )

## sort by publication year
mine.sort( key = lambda publication: publication.year, reverse=True )

mine = map( lambda publication: to_dict( publication ), mine )

## OKM classification

types = {}

for publication in mine:

    for i in 'abcdefghABCDEFGH':
        for j in range(0, 6):
            j = str(j)

            tag = i+j

            if tag in publication['tags']:

                tag = tag.upper()

                if tag not in types:
                    types[ tag ] = []

                types[ tag ].append( publication )

names = {
    'A1' : 'A1 Original research',
    'A2' : 'A2 Literature review',
    'A3' : 'A3 Chapters in research books',
    'A4' : 'A4 Conference proceedings',
    'B1' : 'B1 Unrefereed journal articles',
    'B2' : 'B2 Book section',
    'B3' : 'B3 Unrefereed conference proceedings',
    'C1' : 'C1 Book',
    'C2' : 'C2 Book (editor)',
    'D1' : 'D1 Artikkeli ammattilehdessä',
    'D2' : 'D2 Artikkeli ammatillisessa käsikirjassa',
    'D3' : 'D3 Artikkeli ammatillisessa konferenssijulkaisussa',
    'D4' : 'D4 Julkaistu raportti tai selvitys',
    'D5' : 'D5 Oppikirja',
    'E1' : 'E1 Sanomalehtiartikkeli',
    'E2' : 'E2 Yleistajuinen monografia',
    'F1' : 'F1 Julkaistu itsenäinen taiteellinen teos',
    'F2' : 'F2 Julkinen taiteellinen teoksen osatoteutus',
    'F3' : 'F3 Julkinen taiteellinen esitys tai näyttely',
    'G1' : 'G1 Kandidaatintyö',
    'G2' : 'G2 Pro gradu',
    'G5' : 'G5 Artikkeliväitöskirja',
    'H1' : 'H1 Myönnetty patentti'
}

for key in sorted( names.keys() ):

    if key in types:

        print '###', names[ key ]

        for publication in types[ key ]:
            print '*', to_string( publication )
