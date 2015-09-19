from swagger_spec import *
from urlparse import urlsplit, parse_qs
import datetime, ast
import dateutil.parser
#yourdate = dateutil.parser.parse(datestring)
#print type(ast.literal_eval('True'))
#exit()

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

with open("../api_key_demo.md") as FIN:
    API_KEY = FIN.read().strip()    

url = "https://api.nasa.gov/planetary/earth/imagery?lon=100.75&lat=1.5&date=2014-02-01&cloud_score=True&api_key=DEMO_KEY"

S = Swagger()
p = urlsplit(url)

S.schemes = list(set(S.schemes + [p.scheme]))
S.host = p.netloc
S.basePath = "/"

S.paths[p.path] = path = Path()
x = path.get

query = parse_qs(p.query,keep_blank_values=True)
oper = Operation()
oper.responses = Responses({"200":Response()})
params = oper.parameters
for key,val in query.items():
    
    # Ignore all but first query parameter
    val = val.pop()
    print key,val,infer_type(val)
print S
