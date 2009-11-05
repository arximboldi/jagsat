#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

import sys
sys.path.append ('lib')

from app.jagsat import JagsatApp

if __name__ == '__main__':
    app = JagsatApp ()
    app.run_and_exit ()
