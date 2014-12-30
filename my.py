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

## transfer JUFO tags to something else
for publication in mine:

    jufo = 0

    for i in ['1','2','3']:
        if 'jufo' + i in publication['tags']:
            jufo = i
            publication['tags'].remove( 'jufo' + i )

    publication['jufo'] = jufo

## remove OKM classifications
for publication in mine:

    for i in 'abcdefghABCDEFGH':
        for j in range(0, 6):
            j = str(j)

            tag = i+j

            if tag in publication['tags']:
                publication['tags'].remove( tag )

## sort by tags

tags = {}

for publication in mine:

        tag = 'other'

        if publication['tags']:
            tag = publication['tags'][0]

        if tag not in tags:
            tags[ tag ] = []

        tags[ tag ].append( publication )

out = open('/var/www/main/data/my.json', 'w')
out.write( json.dumps( tags ) )
out.close()
