#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

from tf.behavior import sm

class State (sm.State, object):

    def do_enter_state (self, system = None, *a, **k):    
        self.system = system
        return self.do_enter (*a, **k)
    
    def do_enter (self, *a, **k):
        pass

    def do_exit_state (self):
        return self.do_exit (self)

    def do_exit (self):
        pass

    
