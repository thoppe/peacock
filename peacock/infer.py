from swagger_spec import *
from urlparse import urlsplit, parse_qs
import datetime, ast
import dateutil.parser
import logging
logging.basicConfig(level=logging.INFO)

def infer_type(x):
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
    
    

with open("../api_key_demo.md") as FIN:
    API_KEY = FIN.read().strip()    

url = "https://api.nasa.gov/planetary/earth/imagery?lon=100.75&lat=1.5&date=2014-02-01&cloud_score=True&api_key=DEMO_KEY"

S = Swagger()
p = urlsplit(url)

S.schemes = list(set(S.schemes + [p.scheme]))
S.host = p.netloc
S.basePath = "/"

S.paths[p.path] = path = Path()
path.get.responses = Responses({"200":Response()})

parameters = Parameters()
path.get.parameters = get_parameters(url)

print S
