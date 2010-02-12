#
# Copyright (C) 2009 The JAGSAT project team.
#
# This software is in development and the distribution terms have not
# been decided yet. Therefore, its distribution outside the JAGSAT
# project team or the Project Course evalautors in Abo Akademy is
# completly forbidden without explicit permission of their authors.
#
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


class AutoProxy (object):
    """
    Modified version of:
    
    http://code.activestate.com/recipes/496741/

    This version differs in that setattr and delete are not delegated
    on the proxied class. This allows to easily add data and methods
    in the inherited instance. Also, getattribute is not overriden but
    getattr instead, so the proxy will be accessed *only* if the
    proxy does not override the attribute. This is also implemented for
    special named methods.
    """

    def __init__ (self, proxied):
        self._proxied = proxied

    def __getattr__ (self, name):
        return getattr (self._proxied, name)

    @property
    def proxied (self):
        return self._proxied
    
    _special_names = [
        '__abs__', '__add__', '__and__', '__call__', '__cmp__', '__coerce__', 
        '__contains__', '__delitem__', '__delslice__', '__div__', '__divmod__', 
        '__eq__', '__float__', '__floordiv__', '__ge__', '__getitem__', 
        '__getslice__', '__gt__', '__hash__', '__hex__', '__iadd__', '__iand__',
        '__idiv__', '__idivmod__', '__ifloordiv__', '__ilshift__', '__imod__', 
        '__imul__', '__int__', '__invert__', '__ior__', '__ipow__', '__irshift__', 
        '__isub__', '__iter__', '__itruediv__', '__ixor__', '__le__', '__len__', 
        '__long__', '__lshift__', '__lt__', '__mod__', '__mul__', '__ne__', 
        '__neg__', '__oct__', '__or__', '__pos__', '__pow__', '__radd__', 
        '__rand__', '__rdiv__', '__rdivmod__', '__reduce__', '__reduce_ex__', 
        '__repr__', '__reversed__', '__rfloorfiv__', '__rlshift__', '__rmod__', 
        '__rmul__', '__ror__', '__rpow__', '__rrshift__', '__rshift__', '__rsub__', 
        '__rtruediv__', '__rxor__', '__setitem__', '__setslice__', '__sub__', 
        '__truediv__', '__xor__', 'next',
        '__nonzero__', '__str__', '__repr__',
    ]

    def __new__(cls, obj, *args, **kwargs):
        """
        Creates an proxy instance referencing `obj`. (obj, *args, **kwargs) are
        passed to this class' __init__, so deriving classes can define an 
        __init__ method of their own.

        Note: _class_proxy_cache is unique per deriving class (each
        deriving class must hold its own cache)
        """
        
        try:
            cls_cache = cls.__dict__["_class_proxy_cache"]
        except KeyError:
            cls._class_proxy_cache = cls_cache = {}

        try:
            proxy_cls = cls_cache [obj.__class__]
        except KeyError:
            proxy_cls = cls._create_class_proxy (obj.__class__)
            cls_cache [obj.__class__] = proxy_cls

        ins = object.__new__ (proxy_cls)
        proxy_cls.__init__ (ins, obj, *args, **kwargs)

        return ins

    @classmethod
    def _create_class_proxy (cls, proxied_cls):
        """creates a proxy for the given class"""
        
        def make_method (name):
            def method (self, *args, **kw):
                return getattr (self._proxied, name) (*args, **kw)
            return method
        
        cls_dict = {}
        for name in cls._special_names:
            if hasattr (proxied_cls, name) and not hasattr (cls, name):
                cls_dict [name] = make_method (name)
        
        return type ("%s(%s)" % (cls.__name__, proxied_cls.__name__), (cls,), cls_dict)
