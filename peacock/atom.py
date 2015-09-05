import json
from traits.api import HasPrivateTraits, Disallow, Any
from traits.api import Int, Str, Float, List, Enum, Bool, Dict, Instance

from traits.api import HasTraits, HasStrictTraits

# Traits that are required but missing will be replaced with
# these placeholders.
_default_traits = {
    Str   : "Required string.",
    Int   : -99999,
    Float : -99999.0,
    Bool  : False,
}

class atom(HasPrivateTraits):
    '''
    Extension of traits that allows for required elements
    and has a nice print, and JSON export.
    '''
    
    _required = List
    _conditional_required = {}
    _name_mappings = {}

    def __init__(self,input_dict=None,**kwargs):
    
        if input_dict is not None:
            kwargs.update(input_dict)

        super(HasPrivateTraits,self).__init__(**kwargs)

        # Check if any kwargs were added that are not within the spec
        #defined_keys = self.__getstate__().keys()
        #for key in kwargs:
        #    if key not in defined_keys:
        #        msg = "Key '{}' not defined in class {}."
        #        raise ValueError(msg.format(key,self.__class__.__name__))

        # Add the conditional requirements to the list of required args
        for (key,val),req in self._conditional_required.items():
            if key in kwargs and kwargs[key] in val:
                self._required += req
                
        # Check if all required arguments are present, if not use the default
        '''
        for key in self._required:
            if key not in kwargs:

                trait_obj = self.trait(key).trait_type
                obj_type  = type(trait_obj)

                if obj_type not in _default_traits:                    
                    my_name = self.__class__.__name__
                    trait_name = trait_obj.__class__.__name__
                    msg = 'Trait {} in {} does not have a fallback default.'
                    raise ValueError(msg.format(trait_name, my_name))

                val = _default_traits[obj_type]
                self.set(**{key:val})
        '''

        # Erase the values
        #self._required = None
        #self._conditional_required = None


    def json(self):
        return json.dumps(self.as_dict(),indent=2)

    def __repr__(self):
        return self.json()

    def __nonzero__(self):
        # Only if all subtraits return nonzero too
        #if self._required:
        #    return True
        
        for key,val in self.state().items():
            print "HERE!", key, val
            if val: return True
        return False


    def state(self):
        return vars(self)

    def _valididate_required(self):
        
        for key in self._required:
            if self.get(key)[key] is None:
                my_name = self.__class__.__name__
                trait_obj = self.trait(key).trait_type
                trait_name = trait_obj.__class__.__name__
                msg = "trait '{}' ({}) in {} is a required member can not be undefined."
                raise ValueError(msg.format(key,trait_name,my_name))

    def as_dict(self):
        self._valididate_required()

        output = {}
        obj = self.state()
        
        for key,val in obj.items():

            # Take care of any name mappings
            if key in self._name_mappings:
                key = self._name_mappings[key]

            # If the child is another atom (inherited) then recursively run this
            if atom in val.__class__.__mro__:
                val = val.as_dict()

            # Skip if value is hidden
            if key[0] == "_":
                continue
                
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


if __name__ == "__main__":

    class number(atom):
        value = Float(None)

    class complex(atom):
        x = Instance(number,())

    a = complex()
    print a
    print bool(a)
    print a.x.value
    a.x.value =2
    print a.x.value
    print bool(a)
    print a

    print
    b = complex()
    print b.x.value
    b.x.value = 3223
    print a.x.value, b.x.value


    
    #print help(a)
    
        
