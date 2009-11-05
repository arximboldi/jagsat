#
# This file is copyright Tribeflame Oy, 2009.
#
from PySFML import sf
import os
import weakref
import tf


class SoundFile:

    GAMETICKS_BEFORE_UPDATE_CHECK = 50
    all_soundfiles = weakref.WeakValueDictionary()
    empty_soundfile = None # Modified later

    def __init__(self, filename, magic = False):
        """Do not call this directly."""
        self.soundbuffer = sf.SoundBuffer()
        self.filename = filename
        if not tf.PRODUCTION:
            self.sounds = set()

        self._do_update(0)

        if not tf.PRODUCTION:
            # This makes the stat() checks spread out
            self.last_gametick_updated += \
                ((len(self.all_soundfiles)+1)
                 % self.GAMETICKS_BEFORE_UPDATE_CHECK)

        if magic is True and self.filename not in self.all_soundfiles:
            self.all_soundfiles[self.filename] = self
        else:
            raise tf.TribeFlameException(\
                "Warning, you are not using soundfile.py properly. " + \
                    "Call soundfile.new_soundbuffer instead.")

    def register_sound_usage(self, sound):
        if tf.PRODUCTION:
            return
        self.sounds.add(sound)

    def deregister_sound_usage(self, sound):
        if tf.PRODUCTION:
            return
        self.sounds.remove(sound)

    def new_soundbuffer(filename):
        """
        Loads a new soundbuffer from @filename and returns it.
        Use this function instead of calling the constructor."""
        if filename in SoundFile.all_soundfiles:
            r = SoundFile.all_soundfiles[filename]
            return r
        return SoundFile(filename, magic = True)
    new_soundbuffer = staticmethod(new_soundbuffer)

    def _update(self, gametick):
        if tf.PRODUCTION:
            return
        if self.last_gametick_updated \
                + self.GAMETICKS_BEFORE_UPDATE_CHECK >= gametick:
            return
        self.last_gametick_updated = gametick
        if self.filename is None:
            return
        #print "Sound update check for " + self.filename
        s = os.stat(self.filename)
        if s.st_mtime != self.mtime:
            self._do_update(gametick)

    def _do_update(self, gametick):
        if not tf.PRODUCTION:
            self.last_gametick_updated = gametick

        if self.filename is None:
            return
        if not os.access(self.filename, os.R_OK):
            raise Exception("Sound file " + self.filename + \
                                " can not be read!")
        ok = self.soundbuffer.LoadFromFile(self.filename)
        assert ok

        if not tf.PRODUCTION:
            s = os.stat(self.filename)
            self.mtime = s.st_mtime

            for sound in self.sounds:
                sound._do_sound_updated(self)

    def update_all_soundfiles(thegameloop):
        """Updates sounds from disk in real-time during game play.
        Call this every tick from your main loop. This should only be
        used for faster development, not in production."""
        if tf.PRODUCTION:
            return
        for filename, sound in SoundFile.all_soundfiles.iteritems():
            sound._update(thegameloop.ticks)

    update_all_soundfiles = staticmethod(update_all_soundfiles)

#SoundFile.empty_soundfile = SoundFile.new_soundbuffer(None)


class Sound:

    all_sounds = set()

    def __init__(self, filename):
        sb = SoundFile.new_soundbuffer(filename)
        self._sound = sf.Sound(sb.soundbuffer)
        # Without keeping this ref, SFML stops the sound
        # and thus the AudiotManager removes it.
        self._sb = sb
        Sound.all_sounds.add(self)


class AudioManager:

    def play_sound(self, filename):
        s = self.create_sound(filename)
        s._sound.Play()
        return s

    def create_sound(self, filename):
        s = Sound(filename)
        return s

    def remove_all_sounds(self):
        for sound in Sound.all_sounds:
            sound._sound.Stop()
            sound._sb = None
        Sound.all_sounds.clear()

    def update_audios(self):
        # It is not necessary to call this every tick
        d = set()
        for sound in Sound.all_sounds:
            if sound._sound.GetStatus() == sf.Sound.Stopped:
                print "REMOVING SOUND", sound, sound._sb.filename
                d.add(sound)
                sound._sb = None
        Sound.all_sounds.difference_update(d)
