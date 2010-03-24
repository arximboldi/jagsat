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
    'data/sfx/background/angel-needs-pollution-to-breathe.ogg',
    'data/sfx/background/nebulous-notions.ogg'
    ]

bad_click  = 'data/sfx/clicks/failed_click.wav'
ok_click   = 'data/sfx/clicks/successful_click.wav' 

class button:
    margin    = 5
    class active:
        color     = sf.Color (0, 0, 0)
        border    = sf.Color (0x97, 0xBF, 0x60)
        thickness = 5
        radius    = 15
        text_size = 20
    class inactive (active): pass
    class clicked (active): pass
        
class small_button:
    margin    = 2
    class active:
        color     = sf.Color (0, 0, 0, 200)
        border    = sf.Color (150, 150, 70, 255)
        thickness = 2
        radius    = 15
        text_size = 16
    class inactive (active):
        color     = sf.Color (0, 0, 0, 100)
        border    = sf.Color (0, 0, 0, 0)
    class clicked (inactive):
        pass

class select_button (small_button):
    class selected (small_button.active):
        border    = sf.Color (220, 50, 50, 255)
        color    = sf.Color (50, 0, 0, 200)

class frame (small_button):
    class active (small_button.active):
        thickness = 0

def copy_button_theme (theme):
    class new_theme (theme):
        class active (theme.active): pass
        class inactive (theme.inactive): pass
        class clicked (theme.clicked): pass
    return new_theme

menu   = small_button
player = small_button
