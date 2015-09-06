import peacock
from peacock import *

info = Info()
info.description = "A sample API that uses a petstore as an example to demonstrate features in the swagger-2.0 specification"
info.title = "Swagger Petstore"
info.termsOfService = "http://swagger.io/terms/"
info.contact.name = "Swagger API Team"
info.license.name = "MIT"
info.version = "1.0.0"

res = Response(description="A list of pets.")
res.schema = Schema(type_="array")
res.schema.items = Item(ref_="#/definitions/Pet")

get_pet = Operation()
get_pet.responses = Responses({"200":res})
get_pet.produces  = ["application/json"]
get_pet.description = "Returns all pets from the system that the user has access to"

paths = Paths()
paths["/pets"] = Path(get=get_pet)

pet = Schema(type_="object")
pet.required=["id","name"]

pet.properties["id"] = Property(type="integer",format="int64")
pet.properties["name"] = Property(type="string")
pet.properties["tag"] = Property(type="string")

defs = Definitions()
defs["Pet"] = pet

S = Swagger(info=info,paths=paths,definitions=defs)
S.basePath = "/api"
S.host = "petstore.swagger.io"
S.schemes = ["http"]
S.consumes = ["application/json"]
S.produces = ["application/json"]

print S

if __name__ == "__main__":
    import json

    S1 = json.loads(S.json())
    with open("examples/petstore_minimal.json") as FIN:
        S2 = json.load(FIN)
    
    from deepdiff import DeepDiff
    from pprint import pprint
    diff = DeepDiff(S2,S1)

    if len(diff)>0:
        print diff
        raise SyntaxError("petstore_minimal.json doesn't match!")
    else:
        print "Passes!"

