#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

from core.state import State

class QuittableState (State):

    def quit_state (self):
        self.manager.leave_state (must_quit = True)

    def do_unsink (self, must_quit = False, *a, **k):
        if must_quit:
            self.quit_state ()
