import peacock
from peacock import *
import json

with open("examples/ipify.json") as FIN:
    js = json.load(FIN)

S = peacock.Swagger()
S.update(js)

print S.list_paths()
print S.has_path('/')
print S.get_path('/')
