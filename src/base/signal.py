#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

"""
This module provides a slot-signal mechanism.
"""

from connection import *
from sender import *
from util import *
from meta import *
from proxy import *

class Slot (Destiny):
    """
    A slot is the endpoint of a connection to a signal.
    """
    
    def __init__ (self, func, *a, **k):
        """
        Constructor.

        Parameters:
          - func: The function to be invoked by this slot.
        """
        super (Slot, self).__init__ (*a, **k)
        self.func = func

    def __call__ (self, *args, **kw):
        """
        Invokes the function associated to this slot with the given
        arguments.
        """
        return self.func (*args, **kw)


class Signal (Container):
    """
    This is an event emiter that can be used to remotelly invoke other
    functions, as an instance of the Observer design pattern.
    """
    
    def connect (self, slot):
        """
        This method registers the Slot 'slot' into the signal. If
        'slot' is not a Slot but it is a callable it wraps the
        callable in a Slot. The registered slot is returned. The
        signal works as a list so the new slot will be called after
        all the previously connected slots.
        """

        if not isinstance (slot, Slot): 
            slot = Slot (slot)
        return super (Signal, self).connect (slot)

    def disconnect (self, slot):
        """
        This method disconnects the Slot 'slot' from the signal. If the
        passed argument is not a Slot but a function, it disconnects
        all the slots that wrap that function.
        """
        
        if isinstance (slot, Slot):
            super (Signal, self).disconnect (slot)
        else:
            super (Signal, self).disconnect_if (lambda x: x.func == slot)
        
    def notify (self, *args, **kw):
        """
        Invokes with the arguments passed to this function to all the
        slots that are connected to this signal.
        """
        
        for slot in self._destinies:
            slot (*args, **kw)
    
    def fold (self, folder, start = None):
        """
        Invokes all the connected signal accumulating the result with
        the given 'folder', that will be called on every new
        invocation. The final result provided by the folder will be
        returned after that, or 'start' if no slot was invoked.

        Parameters:
          - folder: Binary function that merges to values values into
            one. The first parameter is the result returned by folder
            in the last call.
          - start: By default this is None. If 'start' is not None, it
            will be treated as a slot return value that is previous to
            any slot in the signal.

        Note: A good idiom is to use acumulator objects as the folder
        function. To do this use the unbounded method that you will
        use to accumulate the values as 'folder' and pass the
        acummulator instance as 'start'.
        """
        
        def executor (ac, func):
            return folder (ac, func ())
            
        if start is None:
            start = self._destinies[0] ()
            return reduce (executor, self._destinies [1:], start)
        else:    
            return reduce (executor, self._destinies, start)
    
    def __iadd__ (self, slot):
        """
        Same as 'connect'.
        """
        self.connect (slot)
        return self
        
    def __call__ (self, *args, **kw):
        """
        Same as 'notify'.
        """
        return self.notify (*args, **kw)


class AutoSignalSender (Sender):
    """
    This can be used to map signals to messages of a sender. The
    intended usage of this is to inherit from this class when you want
    an object to be both a sender.Sender and contain several signals as
    attributes. Whenever you create a signal in your subclass this
    will substitute it by a proxy that invoques the 'send' method of
    the object whenever it is notified, using the attribute name as
    message. This allows, for example, the easy creation of forwarders
    that re-emit the signals if you also inherit from sender.Receiver.
    """
    
    def __setattr__ (self, name, attr):
        """
        Used to inspect every attribute of the object whe it is
        set. If it is a Signal it substitutes the set signal with a
        proxy.
        """
        
        if isinstance (attr, Signal):
            object.__setattr__ (self, name,
                                SenderSignalProxy (attr, self, name))
        else:
            object.__setattr__ (self, name, attr)        
        return attr


class AutoSignalSenderGet (Sender):
    """
    Same as 'AutoSignalSender' but implemented in a different way that
    may incurr in more overhead.
    """
    
    def __getattribute__ (self, name):
        """
        Used to inspect any attribute of the object at retrieval time,
        returning a proxy if it was a Signal.
        """
        
        attr = object.__getattribute__ (self, name)
        if isinstance (attr, Signal):
            return SenderSignalProxy (attr, self, name)
        return attr


class SenderSignal (Signal):
    """
    This signal is modified such that it replies all the notifications
    to a given sender.Sender.
    """
    
    def __init__ (self, sender, message):
        """
        Constructor.

        Parameters:
          - sender: The sender.Sender instance to which this signal
            should notify about its invocation.
          - message: The message name that will be sent to the sender
            when notified.
        """
        
        super (SenderSignal, self).__init__ ()
        self._sender = sender
        self._message = message
    
    def notify (self, *args, **kws):
        """
        Behaves like Signal.notify() but also sends a message through
        the registered sender after calling the slots.
        """
        
        super (SenderSignal, self).notify (self, *args, **kws)
        self._sender.send (self._message, *args, **kws)


class SenderSignalProxy (AutoProxy):
    """
    This proxies a Signal adding the features of SenderSignal to it.
    """
    
    def __init__ (self, signal, sender, message):
        """
        Constructor.

        Parameters:
          - signal: The signal to proxy.
          - sender: The sender.Sender instance to which this signal
            should notify about its invocation.
          - message: The message name that will be sent to the sender
            when notified.
        """

        super (SenderSignalProxy, self).__init__ (signal)
        self._sender = sender
        self._message = message

    def __call__ (self, *args, **kws):
        """
        Class notify.
        """
        self.notify (*args, **kws)

    def notify (self, *args, **kws):
        """
        Invokes the notify method in the proxy but also sends the
        message to the registered sender with the given arguments.
        """
        
        self.proxied.notify (*args, **kws)
        self._sender.send (self._message, *args, **kws)


@instance_decorator
def slot (obj, func):
    """
    This decorator is to be used only with instance methods. When you
    decorate a method with this, it will become an instance of a mixin
    of connection.Trackable and Slot. Also, if the object this method
    belongs to inherits from connection.Tracker, then the slot will be
    automatically registered to it. This is very usefull when you want
    to use a method mainly to receive signals and want tracking
    capabilities so you don't have to keep reference to the signals on
    your own. Still, you can use the method as normally after
    decorated by this.
    """
    
    s = mixin (Trackable, Slot) (lambda *a, **k: func (obj, *a, **k))
    if isinstance (obj, Tracker):
        obj.register_trackable (s)
    return s


@instance_decorator
def signal (obj, func):
    """
    This decorator is to be used only with instance methods. When you
    decorate a method with this, it well become into a modified
    instance of a Signal. This will behave like a normal Signal but it
    will call your decorated method before notifying to the slots, and
    return the value returned by your method, so it can be used
    transparently. Also, if the object this method belongs to is an
    instance of Sender, it will automatically notify it whenever the
    signal is emitted, using the name of the decorated function as the
    message.
    """
    
    if isinstance (obj, Sender) and not \
       isinstance (obj, AutoSignalSenderGet):
        class ExtendedSignal (Signal):
            def notify (self, *args, **kws):
                res = func (obj, *args, **kws)
                obj.send (func.__name__, *args, **kws)
                Signal.notify (self, *args, **kws)
                return res
    else:
        class ExtendedSignal (Signal):
            def notify (self, *args, **kws):
                res = func (obj, *args, **kws)
                Signal.notify (self, *args, **kws)
                return res

    return ExtendedSignal ()


@instance_decorator
def signal_before (obj, func):
    """
    This behaves exactly like the 'signal' decorator, but notifies the
    slots before calling the function and not the other way.
    """
    
    if isinstance (obj, Sender) and not\
       isinstance (obj, AutoSignalSenderGet):
        class ExtendedSignalBefore (Signal):
            def notify (self, *args, **kws):
                obj.send (func.__name__, *args, **kws)
                Signal.notify (self, *args, **kws)
                res = func (obj, *args, **kws)
                return res
    else:
        class ExtendedSignalBefore (Signal):
            def notify (self, *args, **kws):
                Signal.notify (self, *args, **kws)
                res = func (obj, *args, **kws)
                return res
        
    return ExtendedSignalBefore ()