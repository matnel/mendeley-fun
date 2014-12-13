from common import *

import json

session = mendeley()

starred = []

everything = session.documents.iter( page_size = 500, view = 'client', sort = 'created', order = 'asc' )

for publication in everything:

    if publication.starred:
        starred.append( publication )

starred = map( lambda publication: to_dict( publication ), starred )

out = open('/var/www/main/data/star.json', 'w')
out.write( json.dumps( starred ) )
out.close()
