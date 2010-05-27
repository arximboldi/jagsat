#
#  Copyright (C) 2009 TribleFlame Oy
#  
#  This file is part of TF.
#  
#  TF is free software: you can redistribute it and/or
#  modify it under the terms of the GNU General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#  
#  TF is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from tf.gfx import ui
from lxml import etree


class _SimpleHtml:

    def __init__(self, parent, root, width):
        self.parent = ui.VBox(parent)
        self.root = root
        self.width = width
        # So far, width is required
        assert width

        self.sizes = {}
        self.sizes["h1"] = 30
        self.sizes["h2"] = 24
        self.sizes["h3"] = 20
        self.sizes["h4"] = 16
        self.sizes["p"] = 16

        self.padding = {}
        self.padding["h1"] = (0, 10, 10, 10)
        self.padding["h2"] = (0, 10, 5, 10)
        self.padding["h3"] = (0, 10, 5, 10)
        self.padding["h4"] = (0, 10, 5, 10)
        self.padding["p"] =  (0, 10, 5, 40)

    def _create_one_ui(self, child):
        s = None
        if child.tag == "h1":
            s = ui.String(self.parent, unicode(child.text))
            s.set_size(self.sizes["h1"])
            s.set_padding(*self.padding["h1"])
            align = child.get("align")
            if align is not None:
                if align == "center":
#                    x = self.width/2.0 - s._get_width()/2.0
#                    print "SET PADDING", x
#                    s.set_padding(x, x, 0, x)
#                    s.set_margin(x, x, x, x)
                    pass

        elif child.tag == "h2":
            s = ui.String(self.parent, unicode(child.text))
            s.set_size(self.sizes["h2"])
            s.set_padding(*self.padding["h2"])

        elif child.tag == "h3":
            s = ui.String(self.parent, unicode(child.text))
            s.set_size(self.sizes["h3"])
            s.set_padding(*self.padding["h3"])

        elif child.tag == "p":
            # BUG split
            s = ui.MultiLineString(self.parent, unicode(child.text))
            s.set_size(self.sizes["p"])
            s.set_padding(*self.padding["p"])

    def _create_ui_from_xml(self):
        for child in self.root:
            self._create_one_ui(child)
        return self.parent


def create_simple_html(parent, text, width = None):
    assert isinstance(text, unicode)
    t = []
    xml = etree.XMLParser()
    text = unicode("<div>") + text + unicode("</div>")

    print "tf.gfx.htmlhelp TEXT:", type(text), text
    xml.feed(str(text))
    root = xml.close()
    s = _SimpleHtml(parent, root, width)
    return s._create_ui_from_xml()
