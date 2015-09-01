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
    _central_object = None

    def __init__(self,*args,**kwargs):

        super(HasTraits,self).__init__(*args,**kwargs)

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
        self._required = None
        self._conditional_required = None


    def json(self):
        return json.dumps(self.as_dict(),indent=2)

    def __repr__(self):
        return self.json()

    def as_dict(self):

        output = {}

        # If it is a central object there is only one term
        if self._central_object is not None:
            name = self._central_object
            obj  = self.get(name)[name]

        # Otherwise grab the main object and drop the metadata
        else:
            obj = self.__getstate__()
            obj.pop("__traits_version__")
        
        for key,val in obj.items():

            # Take care of any name mappings
            if key in self._name_mappings:
                key = self._name_mappings[key]

            # If the child is another atom (inherited) then recursively run this
            if atom in val.__class__.__mro__:
                val = val.as_dict()
                
            # Always show the output for any True items or numbers set to zero
            if val or val==0:
                output[key] = val
        
        return output

