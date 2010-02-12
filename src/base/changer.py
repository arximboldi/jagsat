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

class Changer (object):
    """
    Data descriptor that allows you to have a value that executes a
    function or function-like object (i.e. a signal) whenever it is
    modified. The function object will be called with two parameters,
    the first one being the object whose this descriptor belongs to,
    and then the new value that is asigned to it.
    """
    
    def __init__ (self,
                  func = None,
                  value = None,
                  *a, **k):
        """
        Constructor.

        Parameters:
          - signal: The function object.
          - value:  Initial value, None by default.
        """
        assert func
        super (Changer, self).__init__ (*a, **k)
        
        self._signal = func
        self._name = '__Changer_' + str (id (self))
        self._default = value

    def __get__ (self, obj, cls):
        return getattr (obj, self._name, self._default)

    def __set__ (self, obj, value):
        setattr (obj, self._name, value)
        self._signal (obj, value)


class InstChanger (Changer):

    def __init__ (self,
                  name = None,
                  value_ = None,
                  *a, **k):
        super (InstChanger, self).__init__ (
            func  = lambda obj, val: getattr (obj, name) (obj, val),
            value = value_)
