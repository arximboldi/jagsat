#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

"""
This module provides a way to send different messages named objects
between objects.
"""

from connection import *

class Receiver (Destiny):
    """
    A Receiver can be used to handle the messages emited by a
    sender. Whenever a message is emited from a sender to which the
    receiver is connected, the 'receive' method will be invoqued.
    """
    
    def receive (self, message, *args, **kws):
        """
        Method used to receive messages from a Sender. 'message' is
        the message sent by the receiver and any other parameters are
        passed afterwards. You can provide your own implementation of
        this method. The default behaviour if to invoque the method
        with name 'message' in the receiver object or throw an
        AtttributeError if there is no method with that name in this
        receiver.
        """
        if not hasattr (self, message):
            raise AttributeError ('Uncaugh message: ' + message)
        return getattr (self, message) (*args, **kws)

class Sender (Container):
    """
    A Sender can be used to emit different named messages to different
    Receivers, that can connect to it.
    """
    
    def send (self, message, *args, **kws):
        """
        Sends the message 'message' to all the receivers that are
        connected. Any other arguments that are passed to this
        function will be sent to the receivers as well.
        """
        
        for f in self._destinies:
            f.receive (message, *args, **kws)
