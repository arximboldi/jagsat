#
# This file is copyright Tribeflame Oy, 2009.
#
import tf
from tf.gfx import uihelp
import tf.gfx.widget.debug
from tf.gfx.imagefile import ImageFile
from tf.behavior.soundfile import SoundFile
import traceback
from PySFML import sf

from tf.behavior import keyboard


class EventLoop:

    def __init__(self,
                 gamename,
                 mainwindow,
                 thegameloop,
                 themousestate):
        self.gamename = gamename
        self.thegameloop = thegameloop
        self.mainwindow = mainwindow

        if themousestate is None:
            themousestate = uihelp.MouseState(mainwindow.views)
        self.themousestate = themousestate

        self._add_default_keybindings()

    def _add_default_keybindings(self):
        km = self.thegameloop.get_keyboardmanager()

        ks = keyboard.KeyShortcut(sf.Key.C,
                                  requires_ctrl = True)
        km.create_keyboard_shortcut(\
            None,
            ks,
            lambda x:
                self.thegameloop.stop())

        ks = keyboard.KeyShortcut(sf.Key.S)
        km.create_keyboard_shortcut(\
            None,
            ks,
            lambda x:
                tf.gfx.widget.debug.create_screenshot(\
                self.mainwindow,
                self.gamename))

    def loop(self):
        while self.thegameloop.is_running():
            self.loop_once()

    def _loop_once(self):
        self.thegameloop.do_game_loop()

        self.themousestate.tick(self.thegameloop)

        event = sf.Event()
        while self.mainwindow.window.GetEvent(event):
            if event.Type == sf.Event.Closed:
                self.thegameloop.stop()

            elif event.Type == sf.Event.KeyPressed \
                   and event.Key.Code == sf.Key.I:
                tf.gfx.widget.debug.dump_information(\
                    self.mainwindow)

            elif event.Type == sf.Event.KeyPressed:
                print "KeyPressed (code, alt, ctrl, shift)", \
                    event.Key.Code, \
                    event.Key.Alt, \
                    event.Key.Control, \
                    event.Key.Shift
                km = self.thegameloop.get_keyboardmanager()
                km.call_key(event.Key.Code,
                            event.Key.Alt,
                            event.Key.Control,
                            event.Key.Shift)
            elif event.Type == sf.Event.Resized:
                print "Event: Resized"
                #recalculate_views(configuration.mainwindow)
                pass
            elif event.Type == sf.Event.LostFocus:
                print "Event: LostFocus "
            elif event.Type == sf.Event.GainedFocus:
                print "Event: GainedFocus"
            elif event.Type == sf.Event.TextEntered:
                print "Event: TextEntered"
            elif event.Type == sf.Event.KeyReleased:
                print "Event: KeyReleased"
            elif event.Type == sf.Event.MouseWheelMoved:
                print "Event: MouseWheelMoved"
            elif event.Type == sf.Event.MouseButtonPressed:
                self.themousestate.mousebutton_pressed(self.thegameloop,
                                                       event)
            elif event.Type == sf.Event.MouseButtonReleased:
                self.themousestate.mousebutton_released(self.thegameloop,
                                                        event)
            elif event.Type == sf.Event.MouseMoved:
                self.themousestate.mouse_move(self.thegameloop,
                                              event)
            elif event.Type == sf.Event.MouseEntered:
                print "Event: MouseEntered"
            elif event.Type == sf.Event.MouseLeft:
                print "Event: MouseLeft"
            elif event.Type == sf.Event.JoyButtonPressed:
                print "Event: JoyButtonPressed"
            elif event.Type == sf.Event.JoyButtonReleased:
                print "Event: JoyButtonReleased"
            elif event.Type == sf.Event.JoyMoved:
                print "Event: JoyMoved"
            else:
                print "Unknown event", event.Type
                assert 0

        for v in self.mainwindow.views:
            v.tick(self.thegameloop)

        self.thegameloop._actionmanager.tick_actions(self.thegameloop)

        ##### DRAW GAME

        self.mainwindow.clear(sf.Color.Black)
        for v in self.mainwindow.views:
            v.draw(self.mainwindow)

        ##### BOOKKEEPING

        ImageFile.update_all_images(self.thegameloop)
        SoundFile.update_all_soundfiles(self.thegameloop)

        self.thegameloop.get_audiomanager().update_audios()

        # DISPLAY

        self.mainwindow.window.Display()

    def loop_once(self):
        try:
            self._loop_once()
        except SystemExit:
            raise
        except (Exception, ), e:
            s = traceback.format_exc()
            s = unicode(s, "UTF-8")
            try:
                lr = self.mainwindow.views[-1].layers[-1]
                tf.gfx.widget.debug.create_error(s,
                                                 lr)
            except IndexError, e:
                print "(FIXME, USE LOG), ERROR: ", s
