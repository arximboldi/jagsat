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

import unittest
from base.observer_old import *

TEST_SIGNALS = ["sig_one", "sig_two", "sig_three"]

class SubjectTester: pass
class ListenerTester: pass
subject (SubjectTester, TEST_SIGNALS)
listener (ListenerTester, TEST_SIGNALS, "ok")

CleverSubjectTester, CleverListenerTester = make_clever_observer (
    TEST_SIGNALS, defret = "ok")

class LightSubjectTester: pass
class LightListenerTester: pass
light_observer (LightSubjectTester, LightListenerTester, TEST_SIGNALS)

class TestListenerOld (unittest.TestCase):

    KLASS = ListenerTester

    def setUp (self):
        self.listener = self.KLASS ()

    def tearDown (self):
        del self.listener
        
    def test_listener_methods (self):
        self.assertEqual (hasattr (self.listener, 'handle_sig_one'), True)
        self.assertEqual (hasattr (self.listener, 'handle_sig_two'), True)
        self.assertEqual (hasattr (self.listener, 'handle_sig_three'), True)

    def test_listener_returns (self):
        self.assertEqual (self.listener.handle_sig_one (), "ok")
        self.assertEqual (self.listener.handle_sig_two (), "ok")
        self.assertEqual (self.listener.handle_sig_three (), "ok")

class TestSubjectOld (unittest.TestCase):

    KLASS = SubjectTester
    
    def setUp (self):
        self.observer = self.KLASS ()

    def tearDown (self):
        del self.observer

    def test_observer_signals (self):
        self.assertEqual (hasattr (self.observer, 'on_sig_one'), True)
        self.assertEqual (hasattr (self.observer, 'on_sig_two'), True)
        self.assertEqual (hasattr (self.observer, 'on_sig_three'), True)
        self.assertEqual (hasattr (self.observer, 'add_listener'), True)
        self.assertEqual (hasattr (self.observer, 'del_listener'), True)
        self.assertEqual (hasattr (self.observer, 'clear'), True)


class TestCleverListenerOld (TestListenerOld):
    
    KLASS = CleverListenerTester


class TestCleverSubjectOld (TestSubjectOld):
    
    KLASS = CleverSubjectTester


class TestObserverOld (unittest.TestCase):

    LISTENER_KLASS = ListenerTester
    SUBJECT_KLASS = SubjectTester
    
    class Counter:
        def __init__ (self, val = 0):
            self.val = 0
        def increase (self):
            self.val += 1
        def decrease (self):
            self.val -= 1
            
    def setUp (self):
        self.lst = self.LISTENER_KLASS ()
        self.sub = self.SUBJECT_KLASS ()

    def tearDown (self):
        del self.sub
        del self.lst

    def test_add_listener (self):
        self.sub.add_listener (self.lst)
        self.assertEqual (self.sub.on_sig_one.count, 1)
        self.assertEqual (self.sub.on_sig_two.count, 1)
        self.assertEqual (self.sub.on_sig_three.count, 1)

    def test_del_listener (self):
        self.test_add_listener ()
        self.sub.del_listener (self.lst)
        self.assertEqual (self.sub.on_sig_one.count, 0)
        self.assertEqual (self.sub.on_sig_two.count, 0)
        self.assertEqual (self.sub.on_sig_three.count, 0)


class TestCleverObserverOld (TestObserverOld):

    LISTENER_KLASS = CleverListenerTester
    SUBJECT_KLASS = CleverSubjectTester

    def test_disconnect_all (self):
        self.sub.add_listener (self.lst)
        self.lst.disconnect ()
        self.assertEqual (self.sub.on_sig_one.count, 0)
        self.assertEqual (self.sub.on_sig_two.count, 0)
        self.assertEqual (self.sub.on_sig_three.count, 0)


class TestLightObserverOld (TestObserverOld):

    class Counter (LightListenerTester):
        def __init__ (self):
            self.value = 0
            
        def handle_sig_one (self):
            self.value += 1

        def handle_sig_two (self):
            self.value -= 1
            
    LISTENER_KLASS = Counter
    SUBJECT_KLASS = LightSubjectTester
    
    def test_add_listener (self):
        self.sub.add_listener (self.lst)
        self.assertEqual (len (self.sub._listeners), 1)
        
    def test_del_listener (self):
        self.test_add_listener ()
        self.sub.del_listener (self.lst)
        self.assertEqual (len (self.sub._listeners), 0)

    def test_signaling (self):
        self.test_add_listener ()
        self.sub.on_sig_one ()
        self.assertEqual (self.lst.value, 1)
        self.sub.on_sig_two ()
        self.assertEqual (self.lst.value, 0)
