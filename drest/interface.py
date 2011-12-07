
from drest.core import exc

class Interface(object):
    def __init__(self):
        """
        An interface definition class.  All Interfaces should subclass from
        here.  Note that this is not an implementation and should never be
        used directly.
        """
        raise exc.dRESTInterfaceError("Interfaces can not be used directly.")
            
class Attribute(object):
    def __init__(self, description):
        """
        An interface attribute definition.
        
        Required Arguments:
        
            description
                The description of the attribute.
                
        """
        self.description = description
    
    def __repr__(self):
        return "<interface.Attribute - '%s'>" % self.description
        
def validate(interface, obj, members, **kw):
    """
    A wrapper to validate interfaces.
    
    Required Arguments:
    
        interface
            The interface class to validate against
            
        obj
            The object to validate.
            
        members
            The object members that must exist.
            
    """
    invalid = []

    for member in members:
        if not hasattr(obj, member):
            invalid.append(member)
            
    if invalid:
        raise exc.dRESTInterfaceError("Invalid or missing: %s in %s" % \
                                      (invalid, obj))