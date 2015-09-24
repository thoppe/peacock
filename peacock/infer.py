from swagger_spec import *
from urlparse import urlsplit, parse_qs
import datetime, ast
import dateutil.parser
import logging
import requests

import bs4
#import requests_cache
#requests_cache.install_cache('debug_cache')

logging.basicConfig(level=logging.INFO)

def infer_type(x):
    '''
    Given a python object x, tries to infer the type using ast.
    This should return proper ints,floats,bools,strs,unicodes.
    If that fails try to return a datetime.
    If all values return a string type.
    '''
    # First try a common type
    try:
        obj = ast.literal_eval(x)
        return type(obj)
    except ValueError:
        pass
    
    # Now try a datetime
    try:
        obj = dateutil.parser.parse(x)
        return type(obj)
    except ValueError:
        pass

    # Got nothing? Return a string
    return str

def get_parameters(url):
    '''
    Returns a list of Swagger parameters from an input url. Types are infered.
    '''
        
    swagger_type_lookup = {
        str : "string",
        unicode : "string",
        float   : "number",
        int     : "integer",
        bool    : "boolean",
        datetime.datetime : "string",
    }

    # Split the query string into key/value pairs
    p = urlsplit(url)
    query = parse_qs(p.query,keep_blank_values=True)

    parameters = []

    for key,val in query.items():
        
        # Ignore all but first query parameter (e.g. if it was called twice)
        val = val.pop()

        # Determine the python type of the object
        obj_type = infer_type(val)

        # Determine the swagger type of the object (this is restricted)
        swagger_type = swagger_type_lookup[obj_type]

        # Set some example text
        text = "Example value: {}".format(val)

        
        p_args = {
            "name"   :key,
            "type000":swagger_type,
            "description":text
        }

        # If the object is a datetime we can set the format
        if obj_type == datetime.datetime:
            p_args["format"] = "date-time"

        # Add the parameter
        parameters.append(Parameter(**p_args))

    return parameters
    
def build_core_swagger_from_url(url):
    S = Swagger()
    p = urlsplit(url)

    S.schemes = list(set(S.schemes + [p.scheme]))
    S.host = p.netloc
    S.basePath = "/"

    return S

def build_get_path(url):
    path = Path()
    path.get.responses  = Responses({"200":Response()})
    path.get.parameters = get_parameters(url)

    # request the url
    r = requests.get(url)
    print r
    if r.status_code == 200:
        print "ROCK AND ROLL!"
    else:
        soup = bs4.BeautifulSoup(r.content, 'html.parser')
        msg = u"url {} failed.\n{}".format(url, soup.text.strip())
        logging.warning(msg)
        
    return path


# For testing load an API key
with open("../api_key_demo.md") as FIN:
    API_KEY = FIN.read().strip()    

url = "https://api.nasa.gov/planetary/earth/imagery?lon=100.75&lat=1.5&date=2014-02-01&cloud_score=True&api_key=DEMO_KEY"

url = url.replace("DEMO_KEY",API_KEY)

S = build_core_swagger_from_url(url)

p = urlsplit(url)
S.paths[p.path] = build_get_path(url)

#print S
