#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

from PySFML import sf

BUTTON_THEME = {
    'active'    : sf.Color (0, 0, 0),
    'inactive'  : sf.Color (128, 128, 128), 
    'border'    : sf.Color (0x97, 0xBF, 0x60),
    'thickness' : 5,
    'margin'    : 8
    }

SMALL_BUTTON_THEME = {
    'active'    : sf.Color (0, 0, 0, 200),
    'inactive'  : sf.Color (128, 128, 128), 
    'border'    : sf.Color (0, 0, 0),
    'thickness' : 3,
    'margin'    : 2
    }

FRAME_THEME = dict (BUTTON_THEME)
FRAME_THEME ['thickness'] = 0

MENU_THEME = {
    'active'    : sf.Color (0, 0, 0, 400),
    'inactive'  : sf.Color (0, 0, 0, 400), 
    'border'    : sf.Color (0, 0, 0),
    'thickness' : 4,
    'margin'    : 6
}

PLAYER_THEME = {
    'active'    : sf.Color (255, 180, 40, 200),
    'inactive'  : sf.Color (127, 127, 127, 200), 
    'border'    : sf.Color (0, 0, 0,200),
    'thickness' : 2,
    'margin'    : 6
}
