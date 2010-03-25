#
#  Copyright (C) 2009 The JAGSAT project team.
#
#  This software is in development and the distribution terms have not
#  been decided yet. Therefore, its distribution outside the JAGSAT
#  project team or the Project Course evalautors in Abo Akademy is
#  completly forbidden without explicit permission of their authors.
#

from base.signal import weak_slot
from base.util  import lazyprop, nop
from base.log   import get_log
from base       import conf

from core.state import State
from core       import task

from ui import music
from ui import widget
from ui import theme
from ui import dialog

from PySFML import sf
from tf.gfx import ui
from tf.gfx.widget import basic

_log = get_log (__name__)

test_playlist = [ 'data/sfx/clicks/failed_click.wav',
                  'data/sfx/clicks/failed_click2.wav',
                  'data/sfx/clicks/successful_click.wav',
                  'data/sfx/clicks/successful_click2.wav' ]


class RootSubstate (State):

    @lazyprop
    def root (self):
        result = self.manager.current
        while result and not isinstance (result, RootState):
            result = result.parent_state
        return result

class RootState (State):

    def do_setup (self, *a, **k):
        super (RootState, self).do_setup (*a, **k)

        cfg_music = conf.GlobalConf ().child ('global-music')
        cfg_music.on_conf_change += self._on_music_change
        self._music = self.tasks.add (
            music.MusicPlayer (self.manager.system.audio))
        if cfg_music.value:
            self._music.play ()

        system = self.manager.system
        self.ui_layer = ui.Layer (system.view)
        self.ui_layer.zorder = 1
        
        self.ui_bg = widget.Background (self.ui_layer)
        self._ui_bg_disabled = True

        self.ui_keyboard = basic.Keyboard (self.ui_layer, theme.keyboard)

        # HACK
        widget.get_keyboard_input = self._get_keyboard_input
                
        self.manager.enter_state ('main_menu')

    @weak_slot
    def _on_music_change (self, cfg):
        if cfg.value and self._music.state != music.state.playing:
            self._music.play ()
        elif not cfg.value and self._music.state != music.state.idle:
            self._music.stop ()

    def _get_keyboard_input (self, originstr, callback):
        self.enable_bg ()
        def callback_wrapper (ev):
             self.disable_bg ()
             callback (ev.text)
        self.ui_keyboard.show_keyboard_and_inject_answer (
             originstr, callback_wrapper, nop)


    def do_release (self):
        super (RootState, self).do_release ()
        self.ui_bg.remove_myself ()

    def do_unsink (self, *a, **k):
        self.manager.leave_state ()
    
    def disable_bg (self):
        if not self._ui_bg_disabled:
            self._ui_bg_disabled = True
            self.ui_bg.set_enable_hitting (False)
            return self.tasks.add (self.ui_bg.fade_out ())
        return self.tasks.add (lambda t: None)

    def enable_bg (self):
        if self._ui_bg_disabled:
            self._ui_bg_disabled = False
            self.ui_bg.set_enable_hitting (True)
            return self.tasks.add (self.ui_bg.fade_in ())
        return self.tasks.add (lambda t: None)


class RootDialogState (RootSubstate):

    def do_setup (self, mk_dialog = None, *a, **k):
        assert mk_dialog
        self.root.enable_bg ()
        self._dialog = mk_dialog (self.root.ui_layer, *a, **k)
        self._dialog.on_dialog_exit += self._on_dialog_exit
        self._dialog.set_center_rel (.5, .5)
        self._dialog.set_position_rel (.5, .5)

    @property
    def dialog (self):
        return self._dialog
    
    @weak_slot
    def _on_dialog_exit (self, ret):
        self.manager.leave_state (dialog_ret = ret)

    def do_release (self):
        super (RootDialogState, self).do_release ()
        self._dialog.remove_myself ()
        self.root.disable_bg ()


class RootYesNoDialogState (RootDialogState):

    def do_setup (self,
                  message = '',
                  yes_ret = 'yes',
                  no_ret  = 'no',
                  *a, **k):
        super (RootYesNoDialogState, self).do_setup (
            lambda parent: dialog.YesNoDialog (parent, message),
            *a, **k)
        self.yes_ret = yes_ret
        self.no_ret  = no_ret

    @weak_slot
    def _on_dialog_exit (self, ret):
        if ret == 'yes':
            self.manager.leave_state (dialog_yes = self.yes_ret)
        else:
            self.manager.leave_state (dialog_no  = self.no_ret)


class RootMessageState (RootSubstate):

    def do_setup (self, message = '', *a, **k):
        super (RootMessageState, self).do_setup (*a, **k)
        
        self.ui_text = ui.MultiLineString (self.root.ui_layer,
                                           unicode (message))
        self.ui_text.set_center_rel (.5, .5)
        self.ui_text.set_position_rel (.5, .5)
        self.ui_text.set_size (50)

        self.root.enable_bg ()
        self.tasks.add (task.sequence (
            self.make_fade_task (task.fade),
            task.run (lambda: self.root.ui_bg.on_click.connect (
                self.on_click_bg))))
    
    @weak_slot
    def on_click_bg (self):
        self.root.disable_bg ()
        self.tasks.add (task.sequence (
            self.make_fade_task (task.invfade),
            task.run (self.manager.leave_state)))

    def make_fade_task (self, fade_task):
        return fade_task (lambda x:
                          self.ui_text.set_color (sf.Color (255,255,255,x*255)),
                          init = True, duration = .75)
