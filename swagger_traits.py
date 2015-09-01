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

class Parameter(atom):
    name = Str()
    in_   = Enum(["query", "header", "path", "formData", "body"])
    description = Str()
    required = Bool()
    _required = ["name","in"]
    
#A = License(name=u"test_project",url='http日本')
X = Info(title="test_project",version="1.0")
S = Swagger(info=X,in_="query")
print S


