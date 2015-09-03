import json
from traits.api import HasTraits
from traits.api import Instance, Int, Str, Float, List, Enum, Bool


class atom(HasTraits):
    '''
    Extension of traits that allows for required elements and has a nice print,
    and JSON export.
    '''
    
    _required = []
    _conditional_required = {}
    _name_mappings = {}

    def __init__(self,input_dict=None,**kwargs):
        if input_dict is not None:
            kwargs.update(input_dict)
        
        super(HasTraits,self).__init__(**kwargs)

        # Check if any kwargs were added that are not within the spec
        defined_keys = self.__getstate__().keys()
        for key in kwargs:
            if key not in defined_keys:
                msg = "Key '{}' not defined in class {}."
                raise ValueError(msg.format(key,self.__class__.__name__))

        # Add the conditional requirements to the list of required args
        for (key,val),req in self._conditional_required.items():
            if key in kwargs and kwargs[key] in val:
                self._required += req

        # Check if all required arguments are present
        for key in self._required:
            if key not in kwargs:
                msg = "Key '{}' in class {} is required."
                raise ValueError(msg.format(key,self.__class__.__name__))

        # Erase the values
        #self._required = None
        #self._conditional_required = None


    def json(self):
        return json.dumps(self.as_dict(),indent=2)

    def __repr__(self):
        return self.json()

    def state(self):
        obj = self.__getstate__()
        obj.pop("__traits_version__")
        return obj

    def as_dict(self):

        output = {}

        obj = self.state()
        
        for key,val in obj.items():

            # Take care of any name mappings
            if key in self._name_mappings:
                key = self._name_mappings[key]

            # If the child is another atom (inherited) then recursively run this
            if atom in val.__class__.__mro__:
                val = val.as_dict()
                
            # Always show the output for any True items or numbers set to zero
            if val or val==0 or key in self._required:
                output[key] = val
        
        return output

class simple_atom(atom):
    '''
    Class with single trait of type:
         data = Dict(Str, TRAIT)
    Simplified init that allows a dictionary to be passed in or keywords.
    '''
    def __init__(self,input_dict=None,**input_kwargs):
        data = {}
        if input_dict is not None:
            data.update(input_dict)
        data.update(input_kwargs)
        super(atom,self).__init__(data=data)
    
    def state(self):
        obj  = self.get("data")["data"]
        return obj
