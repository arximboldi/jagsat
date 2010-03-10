#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

from PySFML import sf

background_music = [
    'data/sfx/background/right-of-freedom.ogg',
    'data/sfx/background/the-age-of-innocence.ogg',
    'data/sfx/background/les-lois-du-ciel.ogg',
    'data/sfx/background/scene-pour-orchestre.ogg',
    'data/sfx/background/confrontation.ogg',
    'data/sfx/background/apprentissage.ogg',
    ]

bad_click  = 'data/sfx/clicks/failed_click.wav'
ok_click   = 'data/sfx/clicks/successful_click.wav' 

button = {
    'active'    : sf.Color (0, 0, 0),
    'inactive_border' : sf.Color (100, 100, 100),
    'inactive'  : sf.Color (128, 128, 128), 
    'border'    : sf.Color (0x97, 0xBF, 0x60),
    'thickness' : 5,
    'margin'    : 8
    }

small_button = {
    'active'    : sf.Color (0, 0, 0, 200),
    'inactive'  : sf.Color (0, 0, 0, 100),
    'border'    : sf.Color (150, 150, 70, 255),
    'inactive_border' : sf.Color (0, 0, 0, 0),
    'thickness' : 2,
    'margin'    : 2
    }

frame = dict (button)
frame ['thickness'] = 0

menu = {
    'active'    : sf.Color (0, 0, 0, 400),
    'inactive'  : sf.Color (0, 0, 0, 400), 
    'border'    : sf.Color (0, 0, 0),
    'thickness' : 4,
    'margin'    : 6
}

player = {
    'active'    : sf.Color (255, 180, 40, 200),
    'inactive'  : sf.Color (127, 127, 127, 200), 
    'border'    : sf.Color (0, 0, 0,200),
    'thickness' : 2,
    'margin'    : 6
}
