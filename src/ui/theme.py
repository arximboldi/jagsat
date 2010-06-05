#
#  Copyright (C) 2009, 2010 JAGSAT Development Team (see below)
#  
#  This file is part of JAGSAT.
#  
#  JAGSAT is free software: you can redistribute it and/or
#  modify it under the terms of the GNU General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#  
#  JAGSAT is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#  
#  JAGSAT Development Team is:
#    - Juan Pedro Bolivar Puente
#    - Alberto Villegas Erce
#    - Guillem Medina
#    - Sarah Lindstrom
#    - Aksel Junkkila
#    - Thomas Forss
#

from PySFML import sf

player_color = {
    0: sf.Color.Blue,
    1: sf.Color (0, 230, 0),
    2: sf.Color.Red,
    3: sf.Color (255, 220, 0),
    4: sf.Color.Black,
    5: sf.Color.Magenta }

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
        border    = sf.Color (0x67, 0x9F, 0x30, 200)
        #border    = sf.Color (0x97, 0x90, 0xBF, 200)
        thickness = 5
        radius    = 15
        text_size = 20
    class inactive (active): pass
    class clicked (active): pass

class keyboard:
    directory = 'data/key/'
    class blackbox (button.active): pass
    class whitebox (button.active):
        thickness = 2
        #border    = sf.Color (255, 100, 100, 64)
        color     = sf.Color (255, 255, 255, 44)

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

class small_button_green (select_button):
    class active (small_button.active):
        border    = button.active.border

line_edit = select_button

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
