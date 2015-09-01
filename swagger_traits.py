# -*- coding: utf-8 -*-

from atom import atom
from traits.api import Instance, Int, Str, Float

class License(atom):
    name = Str()
    url  = Str()
    _required = ["name"]

class Contact(atom):
    name = Str(None)
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

    
A = License(name=u"bob",url='http日本')
X = Info(title="test",version="1.0",license=A)

