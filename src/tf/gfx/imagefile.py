#
# This file is copyright Tribeflame Oy, 2009.
#
from PySFML import sf
import os
import weakref
import tf


class ImageFile:
    """Class which loads an image from a file, creates a
    PySFML Image object. Can auto-update itself when the file
    changes on disk."""

    GAMETICKS_BEFORE_UPDATE_CHECK = 50
    all_images = weakref.WeakValueDictionary()
    empty_image = None # Modified later

    def __init__(self, filename, magic = False):
        """Do not call this directly."""
        self.img = sf.Image()
        self.filename = filename
        if not tf.PRODUCTION:
            self.sprites = set()

        self._do_update(0)

        if not tf.PRODUCTION:
            # This makes the stat() checks spread out
            self.last_gametick_updated += \
                ((len(self.all_images)+1)
                 % self.GAMETICKS_BEFORE_UPDATE_CHECK)

        if magic is True and self.filename not in self.all_images:
            self.all_images[self.filename] = self
        else:
            raise tf.TribeFlameException(\
                "Warning, you are not using imagefile.py properly. " + \
                    "Call imagefile.new_image instead.")

    def register_sprite_usage(self, sprite):
        if tf.PRODUCTION:
            return
        self.sprites.add(sprite)

    def deregister_sprite_usage(self, sprite):
        if tf.PRODUCTION:
            return
        self.sprites.remove(sprite)

    def new_image(filename):
        """Loads a new image from @filename and returns it. Use this function
        instead of calling the constructor."""
        if filename in ImageFile.all_images:
            r = ImageFile.all_images[filename]
            return r
        return ImageFile(filename, magic = True)
    new_image = staticmethod(new_image)

    def _update(self, gametick):
        if tf.PRODUCTION:
            return
        if self.last_gametick_updated \
                + self.GAMETICKS_BEFORE_UPDATE_CHECK >= gametick:
            return
        self.last_gametick_updated = gametick
        if self.filename is None:
            return
        #print "Image update check for " + self.filename
        s = os.stat(self.filename)
        if s.st_mtime != self.mtime:
            self._do_update(gametick)

    def _do_update(self, gametick):
        if not tf.PRODUCTION:
            self.last_gametick_updated = gametick

        if self.filename is None:
            return
        if not os.access(self.filename, os.R_OK):
            raise Exception("Image file " + self.filename + \
                                " can not be read!")
        ok = self.img.LoadFromFile(self.filename)
        assert ok

        if not tf.PRODUCTION:
            s = os.stat(self.filename)
            self.mtime = s.st_mtime

            for sprite in self.sprites:
                sprite._do_image_updated(self)

    def update_all_images(thegameloop):
        """Updates images from disk in real-time during game play.
        Call this every tick from your main loop. This should only be
        used for faster development, not in production."""
        if tf.PRODUCTION:
            return
        for filename, image in ImageFile.all_images.iteritems():
            image._update(thegameloop.ticks)

    update_all_images = staticmethod(update_all_images)

ImageFile.empty_image = ImageFile.new_image(None)
