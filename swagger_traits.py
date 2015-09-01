# -*- coding: utf-8 -*-

from atom import atom
from traits.api import Instance, Int, Str, Float, List, Enum, Bool

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

class Swagger(atom):
    swagger = Str(2.0)
    info = Instance(Info)
    host = Str()
    basePath = Str()
    schemes = Enum([None,"http", "https", "ws", "wss"])
    consumes = List(Str())
    produces = List(Str())
    #paths = Instance(Paths)
    #definitions = Instance(Definitions)
    #parameters = Instance(Parameters)
    #responses = Instance(Responses)
    #securityDefinitions = Instance(SecurityDefinitions)
    #security = Instance(security)
    #tags = Instance(tags)
    #externalDocs = Instance(ExternalDocs)
    #_required=["paths","info","swagger"]

class Item(atom):
    type_   = Enum([None,"string","number","integer","boolean","array","file"])
    format  = Str()
    allowEmptyValue = Bool(None)
    collectionFormat = Enum([None,"csv","ssb","tsv","pipes","multi"])
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
Item.add_class_trait('items', Instance(Item))
    

class Parameter(Item):
    name = Str()
    description = Str()
    required = Bool(None)

    in_   = Enum(["query", "header", "path", "formData", "body"])
    #schema = Instance(Schema)
        
    _required = ["name","in_"]
    
    _conditional_required = {
        ("in_",("body",)):["schema"],
        ("in_",("query", "header", "path", "formData",)):["type_"],
    }
    _conditional_required.update(Item._conditional_required)
    

#A = License(name=u"test_project",url='http日本')
X = Info(title="test_project",version="1.0")
S = Swagger(info=X,in_="query")
P = Parameter(name="foo",in_="query",type_="string")
P.maximum = 20.2

print P



