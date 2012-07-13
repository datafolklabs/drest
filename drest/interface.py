
from . import exc

class Interface(object):
    """
    This is an abstract base class that all interface classes should 
    subclass from.
    
    """
    def __init__(self):
        """
        An interface definition class.  All Interfaces should subclass from
        here.  Note that this is not an implementation and should never be
        used directly.
        """
        raise exc.dRestInterfaceError("Interfaces can not be used directly.")
            
class Attribute(object):
    """
    Defines an Interface attribute.
    
    Usage:
    
    .. code-block:: python
    
        from drest import interface
        
        class MyInterface(interface.Interface):
            my_attribute = interface.Attribute("A description of my_attribute.")
            
    """
    def __init__(self, description):
        """
        An interface attribute definition.
        
        Required Arguments:
        
            description
                The description of the attribute.
                
        """
        self.description = description
    
    def __repr__(self):
        return "Attribute: %s" % self.description
    
    def __str__(self):
        return str(self.__repr__())    
        
def validate(interface, obj, members, metas=[]):
    """
    A wrapper to validate interfaces.
    
    Required Arguments:
    
        interface
            The interface class to validate against
            
        obj
            The object to validate.
            
        members
            A list of object members that must exist.
            
    Optional Arguments:
        
        metas
            A list of meta parameters that must exist.
             
    """
    invalid = []

    for member in members:
        if not hasattr(obj, member):
            invalid.append(member)
            
    if hasattr(obj, '_meta'):
        for meta in metas:
            if not hasattr(obj._meta, meta):
                invalid.append('_meta.%s' % meta)
            
    if invalid:
        raise exc.dRestInterfaceError("Invalid or missing: %s in %s" % \
                                      (invalid, obj))