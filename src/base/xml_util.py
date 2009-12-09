#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

from error import BaseError
from xml.sax.handler import ContentHandler
from xml.sax import SAXException

class XmlError (BaseError): pass

class AutoContentHandler (ContentHandler, object):

    START_ELEMENT_PREFIX      = '_new_'
    END_ELEMENT_PREFIX        = '_end_'
    CHARACTERS_ELEMENT_PREFIX = '_chr_'

    def __init__ (self, *a, **k):
        super (AutoContentHandler, self).__init__ (*a, **k)
        self._name_stack = []
        self._depth = 0
        
    def startElement (self, name, attrs):
        self._name_stack.append (name)
        self.name = name
        self.dispatch_element (False, self.START_ELEMENT_PREFIX, attrs)
        self._depth += 1
        
    def endElement (self, name):
        self.name = name
        self.dispatch_element (True, self.END_ELEMENT_PREFIX)
        self._depth -= 1
        self._name_stack.pop ()

    def characters (self, content):
        self.dispatch_element (True, self.CHARACTERS_ELEMENT_PREFIX, content)

    def dispatch_element (self, silent, prev, *a, **k):
        attr = prev + self._name_stack [-1]
        
        if hasattr (self, attr):
            getattr (self, attr) (*a, **k)
        elif not silent:
            raise SAXException ('Unknown node: ' + self._name_stack [-1])

