import json
from traits.api import HasPrivateTraits, Disallow, Any
from traits.api import Int, Str, Float, List, Enum, Bool, Dict, Instance
from traits.api import HasTraits, HasStrictTraits
import traits

class atom(HasPrivateTraits):
    '''
    Extension of traits that allows for required elements
    and has a nice print, and JSON export.
    '''
    
    _required = List
    _conditional_required = {}
    _name_mappings = {}
    _inv_name_mappings = {}

    def __init__(self,input_dict=None,**kwargs):

        '''
        if input_dict is not None:
            kwargs.update(input_dict)
        super(HasPrivateTraits,self).__init__(**kwargs)
        '''
        super(HasPrivateTraits,self).__init__()

        # Set the inverse name mappings
        self._inv_name_mappings = dict(zip(self._name_mappings.values(),
                                           self._name_mappings.keys()))
        
        if input_dict is not None:
            self.update(input_dict)
        self.update(kwargs)    

        # Check if any kwargs were added that are not within the spec
        # (this is now done by subclassing "HasPrivateTraits"

        # Add the conditional requirements to the list of required args
        for (key,val),req in self._conditional_required.items():
            if key in kwargs and kwargs[key] in val:
                self._required += req

    def update(self, input_dict):
        
        for key,val in input_dict.items():

            keyx = self.get_inv_name(key)
            trait = self.trait(keyx)
            
            if type(trait.trait_type) == traits.trait_types.Instance:
                klass = trait.trait_type.klass
                obj = klass()
                obj.update(val)
                val = obj
                
            self.set(**{keyx:val})

    def json(self):
        return json.dumps(self.as_dict(),indent=2)

    def __repr__(self):
        return self.json()

    def __nonzero__(self):
        # Only if all subtraits return nonzero too
        #if self._required:
        #    return True
        
        for key,val in self.state().items():
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

    def get_name(self,name):
        if name in self._name_mappings:
            return self._name_mappings[name]
        return name

    def get_inv_name(self,inv_name):
        if inv_name in self._inv_name_mappings:
            return self._inv_name_mappings[inv_name]
        return inv_name

    def as_dict(self):
        self._valididate_required()

        output = {}
        obj = self.state()
        
        for key,val in obj.items():

            # Take care of any name mappings
            key = self.get_name(key)

            # If the child is another atom (inherited) then recursively run this
            MRO = val.__class__.__mro__
            if atom in MRO:
                val = val.as_dict()

            # If the child is a list convert all the items as well
            if traits.trait_handlers.TraitListObject in MRO:
                child_vals = []
                for child in val:
                    child_MRO = child.__class__.__mro__
                    if atom in child_MRO:
                        child_vals.append(child.as_dict())
                    else:
                        child_vals.append(child)
                val = child_vals

            # Skip if value is hidden
            if key[0] == "_":
                continue
                
            # Always show the output for any True items or numbers set to zero
            if val is not None or key in self._required:
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
        return dict(self.data)

    def __getitem__(self, key):
        return self.state()[key]

    def __setitem__(self, key, val):
        self.data[key] = val

    def update(self, input_dict):

        # data key and value traits
        _,trait = self.trait("data").inner_traits

        is_instance = True
        is_instance = type(trait.trait_type) == traits.trait_types.Instance

        for key, val in input_dict.items():
            if is_instance:
                klass = trait.trait_type.klass
                obj = klass()
                obj.update(val)
                val = obj
                
            self[key] = val
        



if __name__ == "__main__":

    class number(atom):
        value = Float(None)

    class complex(atom):
        x = Instance(number,())

    class group(simple_atom):
        data = Dict(Str,number)

    g = group({"bob":number()})
    g["bob"] = number({'value':7})
    print g
    exit()

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
    
        
