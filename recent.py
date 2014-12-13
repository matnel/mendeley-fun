from common import *

import json

session = mendeley()

recent = session.documents.list( page_size = 20, sort = 'created', order = 'desc', view = 'all' )

recent = map( lambda publication: to_dict( publication ), recent.items )

out = open('/var/www/main/data/latest.json', 'w')
out.write( json.dumps( recent ) )
out.close()
