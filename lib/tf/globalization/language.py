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

from tf.parsers.configobj import ConfigObj
from tf import signalslot

import re


def _(msg):
    return msg


class LanguageSupport:
    """
    LanguageSupport is a database object of text translations to different
    languages.

    The given @filename is an .ini file in UTF-8 syntax, consisting of
    a main [languages] section, with each language under separate
    subsections [[*language*]].

    Under each language, list key-value pairs with *key*=*value*. A key should
    be a sequence of small letters separated with periods. If you
    want to, you can enclose a value with " signs.

    Parameteres should be encoded using Python's syntax, e.g.
        info.greet.player="Hello player %(name)s!",
    and then the value should be used
        _ = myLanguageSupport.get_default_language()
        ui.String(_["info.greet.player"] % {"name": player_name})

    For displaying multiline strings, use the
    tf.gfx.ui.MultiLineString (or i18nMultiLineString). Otherwise, use
    tf.gfx.ui.String or tf.gfx.ui.i18nString for single-line strings.

    It is recommended that @filename is "i18n.txt" and at the toplevel
    of your game's directory.

    As an example, a i18n.txt file would be

[languages]

[[en]]
info.greet.player="Hello player %(name)s!"

[[fi]]
info.greet.player="Terve, pelaaja %(name)s!"
    """

    def __init__(self, filename):
        """@filename is the language information file to used, in the format
        described in the class documentation."""
        self.languages = {}
        cfg = ConfigObj(filename,
                        encoding="UTF8",
                        raise_errors = True,
                        interpolation = None)
        langs = cfg['languages']
        for langentry in langs.iteritems():
            lang = langentry[0]
            kv = langs[lang]
            self.languages[lang] = Language(lang, kv)

        # BUG retrieve from global configuration, or LC_***
        self.default_language = "en"

    def get_default_language_string(self):
        """
        Returns the default language string for this computer. Note that
        this is just a string, not a Language object. You may want to call
        @get_default_language directly.
        """
        return self.default_language

    def get_default_language(self):
        """Returns a Language object for the default language of the user."""
        return self.get_language(self.default_language)

    def get_supported_language_strings(self):
        """
        Returns a list of strings of all languages supported by this
        object.
        """
        return self.languages.keys()

    def get_language(self, langstring):
        """
        Returns a Language object for the given language string.
        Languages with a country-specific suffix, such as en_US, will be
        returned if they exist, otherwise the nonsuffix version en will be
        returned (if it exists).
        """
        try:
            return self.languages[langstring]
        except KeyError:
            langstring = re.sub("_.*", "", langstring)
            return self.languages[langstring]


class Language:
    """
    A Language object translates given key values to their corresponding
    values for a given language.

    Usage: myLanguage["my.key"] returns the value.

    It is common to use the _ variable to denote the Language object.

    You do not need to create Language objects yourself. Use a LanguageSupport
    object instead.
    """

    def __init__(self, lang, kv):
        self.lang = lang
        self.kv = kv

    def __getitem__(self, key):
        try:
            s = self.kv[key]
            if not isinstance(s, unicode):
                raise ValueError(\
                    "Language %s, key %s, value %s is not unicode" % \
                        (self.lang, key, s))
            return s
        except KeyError:
            print "tf: no i18n for", self.lang, ", key:", key
            return unicode(key)

all_languages = {}
all_languages["fi"] = {"code": "fi.utf8", "name": u"Suomi"}
all_languages["sv"] = {"code": "sv.utf8", "name": u"Svenska"}
all_languages["en_GB"] = {"code": "en_GB.utf8", "name": u"English (UK)"}
all_languages["en_US"] = {"code": "en_US.utf8", "name": u"English (US)"}
all_languages["en"] = {"code": "en_US.utf8", "name": u"English (US)"}


class LanguageChangeNotifier(object):
    """
    A LanguageChangeNotifier is an object which notifies user interface
    components of language changes. This is useful in a multiplayer context
    if you want your user interface to change according to the current
    players language (in e.g. turn-based games).

    To use, create a LanguageChangeNotifier object and create
    tf.gfx.ui.i18nString and tf.gfx.ui.i18nMultiLineString objects
    that automatically register to your given LanguageChangeNotifier object.
    Then change languages by calling set_language_string.
    """

    def __init__(self, languagesupport, initial_language_string = None):
        assert initial_language_string is None \
            or initial_language_string in all_languages.keys()
        self._languagesupport = languagesupport
        if initial_language_string is None:
            initial_language_string = \
                self._languagesupport.get_default_language_string()
        self._language_string = initial_language_string
        assert self._languagesupport.get_language(self._language_string)
        self.signal_language_changed = signalslot.Signal("LanguageChange")

    def set_language_string(self, langstring):
        assert langstring in all_languages.keys()
        assert self._languagesupport.get_language(langstring)
        self._language_string = langstring
        self.signal_language_changed.call(\
            signalslot.Event("LanguageChangeEvent",
                             language = langstring))
        print "Calling LanguageChangeEvent", \
            langstring, \
            self.signal_language_changed.targets

    def get_language_support(self):
        return self._languagesupport

    def get_language_string(self):
        return self._language_string

    def get_language(self):
        return self._languagesupport.get_language(self._language_string)

    def _register_for_language_change(self,
                                      widget):
        _ = self.get_language()
        value = _[widget.key]
        widget.set_string(value)

        def x(e):
            _ = self.get_language()
            #print "Setting", widget, e.language, widget.key, _[widget.key]
            widget.set_string(_[widget.key])

        self.signal_language_changed.add(x)
