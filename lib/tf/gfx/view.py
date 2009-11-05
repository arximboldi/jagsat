#
# This file is copyright Tribeflame Oy, 2009.
#
from tf.gfx import ui
from tf import signalslot
from tf.behavior.gameloop import get_game_loop

import math


class ViewFocus(object):
    """Abstract base class to move a view around."""

    def __init__(self):
        self.view = None

    def start(self):
        pass

    def tick(self):
        raise NotImplementedError()


class PanToPointFocus(ViewFocus):

    def __init__(self):
        ViewFocus.__init__(self)
        self.ok = True

    def tick(self):
        if self.ok:
            return True

        max_secs = 2.0
        gl = get_game_loop()
        now = gl.now()

        b = now >= self.start_time + max_secs
        if b:
            self.ok = True

        if self.ok:
            return True

        t = (now - self.start_time) / max_secs
        assert t >= 0.0
        assert t <= 1.0
        # t is [0..1]
        r = t * math.pi
        c = math.cos(r)
        dx2 = self.dx / 2.0
        dy2 = self.dy / 2.0
        cx = self.origcx + dx2 - c * dx2
        cy = self.origcy + dy2 - c * dy2
        self.view.recenter_view(cx, cy)
        return b

    def start(self):
        pass

    def stop(self):
        # If user is looking around, don't do anything
        self.ok = True

    def get_center_when_looking_at(self, x, y):
        h = self.view.view.GetHalfSize()
        hx = h[0]
        hy = h[1]
        if x < hx:
            x = hx
        if y < hy:
            y = hy
        if x > self.view.content_width - hx:
            x = self.view.content_width - hx
        if y > self.view.content_height - hy:
            y = self.view.content_height - hy

        return (x, y)

    def focus_on(self, x, y):
        ncx, ncy = self.get_center_when_looking_at(x, y)
        cntr = self.view.view.GetCenter()
        self.origcx = cntr[0]
        self.origcy = cntr[1]
        self.destx = ncx
        self.desty = ncy
        self.dx = self.destx - self.origcx
        self.dy = self.desty - self.origcy
        self.start_time = get_game_loop().now()
        self.ok = False


class PanAroundFocus(ViewFocus):

    def __init__(self):
        ViewFocus.__init__(self)
        self.ok = True

    def start(self):
        gl = get_game_loop()
        now = gl.now()
        self.start_time = now

    def tick(self):
        w = self.view.content_width
        h = self.view.content_height
        hs = self.view.view.GetHalfSize()
        sw = hs[0]
        sh = hs[1]

        a = sw / 2.0
        b = sh / 2.0

        gl = get_game_loop()
        now = gl.now()
        dt = now - self.start_time

        t = dt * 0.1

        cx = w / 2.0 + a * math.cos(t) - b * math.sin(t)
        cy = h / 2.0 + a * math.cos(t) + b * math.sin(t)
        self.view.recenter_view(cx, cy)

    def stop(self):
        pass
