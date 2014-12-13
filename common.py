import os
import yaml

from mendeley import Mendeley
from mendeley.session import MendeleySession

def mendeley():

    ## load configs from file
    conf = open('config.yml', 'r+w')
    config = yaml.load( conf )

    mendeley = Mendeley(config['clientId'], config['clientSecret'], config['path'] )

    ## interactive OAuth flow
    if 'token' not in config:
      auth = mendeley.start_authorization_code_flow()
      state = auth.state
      auth = mendeley.start_authorization_code_flow( state = state )
      print auth.get_login_url()

      ## auth = mendeley.start_implicit_grant_flow()
      # After logging in, the user will be redirected to a URL, auth_response.
      session = auth.authenticate( raw_input() )

      print session.token
      config['token'] = session.token

      ## clean file
      conf.write('')
      yaml.dump( config, conf, default_flow_style=False )
      print 'New infos stored'

    ## update access tokens

    ## use new access token
    session = MendeleySession( mendeley, config['token'] )

    return session

def to_dict( publication ):

    data = {}

    data['title'] = publication.title
    data['year'] = publication.year
    data['type'] = publication.type
    data['venue'] = publication.source

    data['authors'] = map( lambda person: { 'forename' : person.first_name , 'surname' : person.last_name } , publication.authors )

    return data
