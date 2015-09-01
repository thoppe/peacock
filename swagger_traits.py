# -*- coding: utf-8 -*-

from atom import atom
from traits.api import Instance, Int, Str, Float, List, Enum, Bool, Any, Dict

class License(atom):
    name = Str()
    url  = Str()
    _required = ["name"]

class Contact(atom):
    name = Str()
    url  = Str()
    emai = Str()

class Info(atom):
    title   = Str()
    version = Str()
    description    = Str()
    termsOfService = Str()
    license = Instance(License)
    contact = Instance(Contact)
    _required = ["title", "version"]

class XMLObject(atom):
    name = Str()
    namespace = Str()
    prefix = Str()
    attribute = Bool(False)
    wrapped   = Bool(None)

class ExternalDocs(atom):
    description = Str()
    url = Str()
    _required = ["url"]

class Tag(atom):
    name = Str()
    description = Str()
    externalDocs = Instance(ExternalDocs)
    _required = ["name"]

class Scopes(atom):
    name = Dict(Str(), Str())
    _central_object = "name"

class SecurityRequirement(atom):
    name = Dict(Str(), List(Str()))
    _central_object = "name"

class SecurityScheme(atom):
    type_ = Enum([None,"basic", "apiKey","oauth2"])
    description = Str()
    name = Str()
    in_ = Enum([None,"query","header"])
    flow = Enum([None, "implicit", "password", "application", "accessCode"])
    authorizationUrl = Str()
    tokenUrl = Str()
    scopes = Instance(Scopes)

    _required = ["type_",]
    _conditional_required = {
        ("type_",("apiKey",)):["name","in_"],
        ("type_",("apiKey",)):["flow","authorizationUrl","tokenUrl","scopes"],
    }
        
class SecurityDefinitions(atom):
    name = Dict(Str(), SecurityScheme)
    _central_object = "name"
        
class Item(atom):
    type_   = Enum([None,"string","number","integer","boolean","array","file"])
    format  = Str()
    allowEmptyValue = Bool(None)
    default = Str()
    maximum = Float(None)
    exclusiveMaximum = Bool(None)
    minimum = Float(None)
    exclusiveMinimum = Float(None)
    maxLength = Int(None)
    minLength = Int(None)
    pattern = Str()
    maxItems = Int(None)
    minItems = Int(None)
    uniqueItems = Bool(None)
    enum = List(Str())
    multipleOf = Float(None)

    _required = ["type_"]
    _conditional_required = {
        ("type_",("array",)):["_items"],
    }
    _name_mappings = {"type_":"type"}
    
Item.add_class_trait('items', Instance(Item))

class Schema(Item):
    ref_ = Str()
    title = Str()
    description = Str()
    required = Bool(None)
    #maxProperties = Str()
    #minProperties = Str()
    #items = List(Instance(Item))
    #properties = ???
    #allOf = ???
    #additionalProperties = ???

    # Further schema documentation
    discriminator = Str()
    readOnly = Bool(None)
    xml = Instance(XMLObject)
    externalDocs = Instance(ExternalDocs)
    example = Any()

    _name_mappings = {"ref_":"$ref"}
    _name_mappings.update(Item._name_mappings)

class Definitions(atom):
    name = Dict(Str(), Instance(Schema))
    _central_object = "name"

###############################################################################################

class Parameter(Item):
    name = Str()
    description = Str()
    required = Bool(None)
    collectionFormat = Enum([None,"csv","ssb","tsv","pipes","multi"])

    in_   = Enum(["query", "header", "path", "formData", "body"])
    schema = Instance(Schema)
        
    _required = ["name","in_"]
    
    _conditional_required = {
        ("in_",("body",)):["schema"],
        ("in_",("query", "header", "path", "formData",)):["type_"],
    }
    _conditional_required.update(Item._conditional_required)
    
    _name_mappings = {"in_":"in"}
    _name_mappings.update(Item._name_mappings)

class Parameters(atom):
    name = Dict(Str(), Parameter)
    _central_object = "name"

###############################################################################################

class Header(Item):
    pass

class Headers(atom):
    name = Dict(Str(), Header)
    _central_object = "name"

class Example(atom):
    mime_type = Dict(Str(),Dict(Str(),Str()))
    _central_object = "mime_type"

class Response(atom):
    description = Str()
    schema = Instance(Schema)
    headers = Instance(Headers)
    examples = Instance(Example)
    _required = ["description"]

class Responses(atom):
    name = Dict(Str(), Response)
    _central_object = "name"
    

###############################################################################################

class Swagger(atom):
    swagger = Str(2.0)
    info = Instance(Info)
    host = Str()
    basePath = Str()
    schemes = Enum([None,"http", "https", "ws", "wss"])
    consumes = List(Str())
    produces = List(Str())
    #paths = Instance(Paths)
    definitions = Instance(Definitions)
    parameters = Instance(Parameters)
    responses = Instance(Responses)
    securityDefinitions = Instance(SecurityDefinitions)
    security = List(Instance(SecurityRequirement))
    tags = Instance(Tag)
    externalDocs = Instance(ExternalDocs)
    #_required=["paths","info","swagger"]

###############################################################################################


#A = License(name=u"test_project",url='http日本')
X = Info(title="test_project",version="1.0")
S = Swagger(info=X,in_="query")
P = Parameter(name="foo",in_="query",type_="string")
P.maximum = 20.2

EX = Example(mime_type={"application/json":{'name':'puma'}})
print Schema(type_="integer")
print S
print P

    
headers = {
    "X-Rate-Limit-Limit": Header(**{
        "description": "The number of allowed requests in the current period",
        "type_": "integer"
    }),
    "X-Rate-Limit-Remaining": Header(**{
        "description": "The number of remaining requests in the current period",
        "type_": "integer"
    }),
    "X-Rate-Limit-Reset": Header(**{
        "description": "The number of seconds left in the current period",
        "type_": "integer"
    })
}


print Headers(name=headers)

data = {"pet_store":["write:pets","read:pets"]}
X = SecurityRequirement(name=data)
print X
exit()
    


