# -*- coding: utf-8 -*-

from atom import atom, simple_atom
from traits.api import Int, Str, Float, List, Enum
from traits.api import Bool, Any, Dict, Either, This
from traits.api import Instance

class License(atom):
    name = Str
    url  = Str
    _required = ["name"]

class Contact(atom):
    name  = Str
    url   = Str
    email = Str

class Info(atom):
    title   = Str
    version = Str
    description    = Str
    termsOfService = Str
    license = Instance(License,())
    contact = Instance(Contact,())
    _required = ["title", "version"]

class XMLObject(atom):
    name = Str
    namespace = Str
    prefix = Str
    attribute = Bool
    wrapped   = Bool

class ExternalDocs(atom):
    description = Str
    url = Str
    _required = ["url"]

class Tag(atom):
    name = Str
    description = Str
    externalDocs = Instance(ExternalDocs,())
    _required = ["name"]

class Scopes(simple_atom):
    data = Dict(Str, Str)

class SecurityRequirement(simple_atom):
    data = Dict(Str, List(Str))

class SecurityScheme(atom):
    type000 = Enum([None,"basic", "apiKey","oauth2"])
    description = Str
    name = Str
    in000  = Enum([None,"query","header"])
    flow = Enum([None, "implicit", "password", "application", "accessCode"])
    authorizationUrl = Str
    tokenUrl = Str
    scopes = Instance(Scopes,())

    _required = ["type000",]
    _conditional_required = {
        ("type000",("apiKey",)):["name","in000"],
        ("type000",("oauth2",)):["flow","authorizationUrl","tokenUrl","scopes"],
    }
    _name_mappings = {"in000":"in", "type000":"type"}
        
class SecurityDefinitions(simple_atom):
    data = Dict(Str, Instance(SecurityScheme,()))
        
class Item(atom):
    ref000    = Str
    type000   = Enum([None,"string","number","integer",
                      "boolean","array","file"])
    format  = Str
    allowEmptyValue = Bool
    default = Str
    maximum = Float
    exclusiveMaximum = Bool
    minimum = Float
    exclusiveMinimum = Float
    maxLength = Int
    minLength = Int
    pattern = Str
    maxItems = Int
    minItems = Int
    uniqueItems = Bool
    enum = List(Str)
    multipleOf = Float

    #_required = ["type000"]
    
    _conditional_required = {
        ("type000",("array",)):["items"],
    }
    _name_mappings = {"type000":"type",
                      "ref000":"$ref"}

    items = Instance(This,())
    
#Item.add_class_trait('items', Instance(Item))

class Reference(atom):
    ref000 = Str
    _name_mappings = {"ref000":"$ref"}
    _required = ["ref000"]


class Property(Item):
    pass

class Properties(simple_atom):
    data = Dict(Str, Instance(Property,()))
    
class Schema(atom):
    ref000 = Either(Str, Instance(Reference,()))
    title = Str
    description = Str
    required = List(Str)
    type000 = Str

    properties = Instance(Properties,())
    #allOf = ???
    #additionalProperties = ???
    #maxProperties = Str
    #minProperties = Str
    items = Instance(Item,())

    # Further schema documentation
    discriminator = Str
    readOnly = Bool
    xml = Instance(XMLObject,())
    externalDocs = Instance(ExternalDocs,())
    example = Any
    
    _name_mappings = {"ref000":"$ref"}
    _name_mappings.update(Item._name_mappings)


class Definitions(simple_atom):
    data = Dict(Str, Instance(Schema,()))

######################################################################

class Parameter(Item):
    name = Str
    description = Str
    required = Bool
    collectionFormat = Enum([None,"csv","ssb","tsv","pipes","multi"])

    in000   = Enum(["query", "header", "path", "formData", "body"])
    schema = Instance(Schema,())
        
    _required = ["name","in000"]
    
    _conditional_required = {
        ("in000",("body",)):["schema"],
        ("in000",("query", "header", "path", "formData",)):["type000"],
    }
    _conditional_required.update(Item._conditional_required)
    
    _name_mappings = {"in000":"in"}
    _name_mappings.update(Item._name_mappings)

class Parameters(simple_atom):
    data = Dict(Str, Instance(Parameter,()))

######################################################################

class Header(Item):
    pass

class Headers(simple_atom):
    data = Dict(Str, Instance(Header,()))

class Example(simple_atom):
    data = Dict(Str,Dict(Str,Str))

class Response(atom):
    description = Str
    schema = Instance(Schema,())
    headers = Instance(Headers,())
    examples = Instance(Example,())
    _required = ["description"]

class Responses(simple_atom):
    data = Dict(Str, Instance(Response,()))

######################################################################

class Operation(atom):
    tags = List(Str)
    summary = Str
    description = Str
    externalDocs = Instance(ExternalDocs,())
    operationId = Str
    consumes = List(Str)
    produces = List(Str)
    parameters = List(Either(Instance(Parameter,()),
                             Instance(Reference,())))
    responses = Instance(Responses,())
    schemes   = List(Enum([None,"http", "https", "ws", "wss"]))
    deprecated = Bool
    security = Instance(SecurityRequirement,())
    _required = ["responses"]

class Path(atom):
    ref000 = Instance(Reference,())
    get  = Instance(Operation,())
    put  = Instance(Operation,())
    post = Instance(Operation,())
    delete  = Instance(Operation,())
    options = Instance(Operation,())
    head = Instance(Operation,())
    patch = Instance(Operation,())
    parameters = List(Either(Parameters,Reference))
    _name_mappings = {"ref000":"$ref"}

class Paths(simple_atom):
    data = Dict(Str, Instance(Path,()))

######################################################################

class Swagger(atom):
    swagger = Str("2.0")
    info = Instance(Info,())
    host = Str
    basePath = Str
    schemes = List(Enum([None,"http", "https", "ws", "wss"]))
    consumes = List(Str)
    produces = List(Str)
    paths = Instance(Paths,())
    definitions = Instance(Definitions,())
    parameters = Instance(Parameters,())
    responses = Instance(Responses,())
    securityDefinitions = Instance(SecurityDefinitions,())
    security = List(Instance(SecurityRequirement,()))
    tags = Instance(Tag,())
    externalDocs = Instance(ExternalDocs,())
    _required=["paths","info","swagger"]

    def has_path(self, path):
        # Returns True if the path is a valid endpoint
        return path in self.paths.keys()

    def list_paths(self):
        return self.paths.keys()

    def get_path(self, path):
        if not self.has_path(path):
            raise KeyError

        return self.paths[path]

######################################################################
