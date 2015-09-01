import json
from traits.api import HasTraits



class atom(HasTraits):
    '''
    Extension of traits that allows for required elements and has a nice print,
    and JSON export.
    '''
    
    _required = []
    
    def __init__(self,*args,**kwargs):
        super(HasTraits,self).__init__(*args,**kwargs)
        state = self.as_dict()
        for key in self._required:
            if key not in kwargs:
                msg = "Key '{}' in class {} is required"
                raise ValueError(msg.format(key,self.__class__.__name__))
            
    def json(self):
        return json.dumps(self.as_dict())

    def __repr__(self):
        return self.json()

    def as_dict(self):
        output = {}
        obj = self.__getstate__()
        obj.pop("__traits_version__")
        for key,val in obj.items():
            if atom in val.__class__.__bases__:
                val = val.as_dict()
            if val or val==0:
                output[key] = val
        return output

