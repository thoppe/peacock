import peacock
from peacock import *
import json

with open("examples/petstore_minimal.json") as FIN:
    js = json.load(FIN)

S = peacock.Swagger()
#print js
#print S
S.update(js)
#print S
print S.list_paths()
print S.has_path('/pets')
print S.get_path('/pets')
