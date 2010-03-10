#
# This file is copyright Tribeflame Oy, 2009.
#
"""
Various helper routines for user interface elements.
"""

from PySFML import sf
from tf.gfx import ui
from tf import signalslot
import math


def sign(x):
    if x < 0.0:
        return -1
    if x > 0.0:
        return 1
    return 0


def clamp_angle(a):
    while a < 0:
        a += 360
    a = a % 360
    return a


def clamp(min, value, max):
    if value < min:
        return min
    if value > max:
        return max
    return value


def dist(x, y):
    return math.sqrt(x * x + y * y)


def ddist(x, y):
    return x * x + y * y


def get_myself_and_parent_chain(s, includeme = True):
    ps = []
    if includeme:
        ps.append(s)
    #assert isinstance(s, ui.Component)
    p = s.parent
    while p:
        assert p != s
        if not isinstance(p, ui.Component):
            return ps
        ps.append(p)
        p = p.parent

    return ps


def get_parent_chain_and_myself(s, includeme = True):
    # BUG This can be made faster
    ps = get_myself_and_parent_chain(s)
    ps.reverse()
    return ps


def get_total_rotation_due_to_parents(widget, includeme = True):
    ps = get_myself_and_parent_chain(widget, includeme)
    rots = [p.GetRotation() for p in ps]
    return sum(rots)


def transform_global_coord_to_local(s, x, y):
    ps = get_parent_chain_and_myself(s)
    tx = x
    ty = y
    for p in ps:
        tx, ty = p.TransformToLocal(tx, ty)
    return tx, ty


def hit_sprite(layer, view, sprite, x, y):
    sz = (sprite._get_width(), sprite._get_height())

    center = sprite.GetCenter()

    tx, ty = transform_global_coord_to_local(sprite, x, y)
    sc = sprite.GetScale()
    tx *= sc[0]
    ty *= sc[1]
    #if hasattr(sprite, "name"):
    #    print "hit?", sprite, tx, ty, sz[0], sz[1]

    shape = sprite.get_hit_shape()
    # BUG should do a fast .RECTANGLE check to everything?
    if shape == ui.HitShape.RECTANGLE:
        hit = 0 <= tx <= sz[0] and 0 <= ty <= sz[1]
    elif shape == ui.HitShape.ELLIPSE:
        hw = sz[0] / 2.0
        hh = sz[1] / 2.0
        dx = (tx - hw) / hw
        dy = (ty - hh) / hh
        dd = dx * dx + dy * dy
        hit = dd < 1.0
    elif shape == ui.HitShape.NONALPHA:
        hit = 0 <= tx <= sz[0] and 0 <= ty <= sz[1]
        if hit:
            c = sprite._sprite.GetPixel(int(tx), int(ty))
            hit = c.a >= 128
    elif shape == ui.HitShape.USERDEFINED:
        hit = sprite.is_hit(tx, ty)
    else:
        assert 0

    if hit:
        return (sprite, tx, ty)
    else:
        return None


def hit_sprite_hierarchy(layer, view, sprite, x, y):
    hits = []
    if sprite.get_visible() is False:
        return hits

    # bug children must be inside parent, or this checking fails.

    hs = hit_sprite(layer, view, sprite, x, y)
    if hs is None:
        return hits
    hits.append(hs)

    for s in sprite.children_back:
        h = hit_sprite_hierarchy(layer, view, s, x, y)
        hits.extend(h)

    for s in sprite.children:
        h = hit_sprite_hierarchy(layer, view, s, x, y)
        hits.extend(h)

    return hits


def hit_sprites(layer, window_x, window_y):
    """
    Returns the set of sprites (tf.gfx.ui.Component) in a @Layer
    that are hit at coordinates @window_x, @window_y
    """
    view = layer._view
    pr = view.window.window.ConvertCoords(window_x, window_y, view.view)
    x = pr[0]
    y = pr[1]

    hits = []

    for s in layer.objects:
        h = hit_sprite_hierarchy(layer, view, s, x, y)
        hits.extend(h)

    # bug stupid if.
    hits = [h for h in hits if h[0]._enable_hitting]

    hits.reverse()

    return hits

# HACK HACK HACK HAK!!
#xratio = 1366./1024
xratio = 1

class MouseState:
    """
    Class that handles the user hitting or dragging something onscreen.
    It is created automatically by tf.behavior.eventloop, so you do not have to
    do it.
    """

    def __init__(self, all_views):
        self.speed_to_click = 10
        self.radius_to_pan = 5

        self.component_info = None # (component, localx, localy)
        self.is_pan = False
        self.all_views = all_views
        self.radius_to_pan *= self.radius_to_pan
        self.start_event = None

    def _component_at(self, event):
        for v in self.all_views[::-1]:
            for layer in v.layers[::-1]:
                hits = hit_sprites(layer,
                                   event.MouseButton.X * xratio,
                                   event.MouseButton.Y)
                if hits:
                    #print "HITS", hits
                    return hits[0]

    def mousebutton_pressed(self, gameloop, event):
        self.ticks = gameloop.ticks
        self.component_info = self._component_at(event)
        self.start_event = (event.MouseButton.X * xratio,
                            event.MouseButton.Y)
        self.is_pan = False

    def tick(self, gameloop):
        # BUG should continue panning a while, depending on the
        # UI effect we want

        # Start panning if time has passed
        if self.component_info and not self.is_pan:
            dt = gameloop.ticks - self.ticks
            if dt > self.speed_to_click:
                self._start_pan()
            elif not self.component_info[0].signal_click.is_enabled():
                # Also start panning if the click is disabled,
                # thus starting the pan much faster.
                self._start_pan()

    # BUG should use local coords

    def _start_pan(self):
        assert self.component_info
        c = self.component_info[0]
        # BUG start_pan is an obsolete interface
        if hasattr(c, "start_pan"):
            #print "START PANNING", self.component
            self.is_pan = True
            c.start_pan(self.start_event)
        else:
            if c.signal_pan.is_enabled():
                self.is_pan = True
                c.signal_pan.call(\
                    signalslot.Event("StartPanEvent",
                                     component = c,
                                     x = self.start_event[0],
                                     y = self.start_event[1]))
            else:
                print "Can't pan on", self.component_info[0], \
                    "I'll click instead on mousereleased"
                #self.component = None
                pass

    def mouse_move(self, gameloop, event):


        if not self.component_info:
            return

        # Start panning if large movement is detected
        if not self.is_pan and self.start_event is not None:
            dx = event.MouseMove.X*xratio - self.start_event[0]
            dy = event.MouseMove.Y - self.start_event[1]
            dist = dx * dx + dy * dy
            if dist >= self.radius_to_pan:
                self._start_pan()

        if self.is_pan:
            #print "PANNING", self.component
            origc = self.component_info[0]
            if origc.signal_pan.is_enabled():
                origc.signal_pan.call(\
                    signalslot.Event("DoPanEvent",
                                     component = origc,
                                     x = event.MouseMove.X *xratio,
                                     y = event.MouseMove.Y))
            else:
                # BUG OBSOLETE DO NOT USE
                self.component_info[0].do_pan((event.MouseMove.X *xratio,
                                               event.MouseMove.Y))

    def mousebutton_released(self, gameloop, event):
        self.start_event = None
        try:
            if not self.component_info:
                return
            c = self._component_at(event)
            if self.is_pan:
                #print "END PAN", self.component
                origc = self.component_info[0]
                if origc.signal_pan.is_enabled():
                    origc.signal_pan.call(\
                        signalslot.Event("EndPanEvent",
                                         component = origc,
                                         x = event.MouseButton.X * xratio,
                                         y = event.MouseButton.Y))
                else:
                    # BUG OBSOLETE DO NOT USE
                    self.component_info[0].end_pan((event.MouseButton.X *xratio,
                                                    event.MouseButton.Y))
            else:
                if c and c[0] == self.component_info[0]:
                    #print "USER HIT", self.component
                    # BUG drop onto "c" component
                    print "uihelp: mousereleased on", self.component_info
                    x = self.component_info[1]
                    y = self.component_info[2]
                    self.component_info[0].user_hit(gameloop, x, y)
        finally:
            self.component_info = None
            self.is_pan = False


class GridInserter:
    """
    Abstract superclass for inserting things into a tf.gfx.grid.
    """

    def __init__(self, grid):
        self.grid = grid


class GridRowInserter(GridInserter):
    """
    Inserts items into a row in the grid.
    """

    def __init__(self, grid, row = 0, automatically_to_next_row = False):
        GridInserter.__init__(self, grid)
        self.idx = 0
        self.row = row
        self.automatically_to_next_row = automatically_to_next_row

    def add_child(self, child):
        if self.automatically_to_next_row and \
                self.idx >= self.grid.get_columns():
            self.row += 1
            self.idx = 0

        assert self.idx < self.grid.get_columns()
        assert self.row < self.grid.get_rows()

        if child:
            self.grid.add_child(child, self.idx, self.row)

        self.idx += 1

    def skip(self, count):
        assert self.idx < self.grid.get_columns()
        self.idx += count
        if self.automatically_to_next_row:
            c = self.grid.get_columns()
            assert c > 0
            while self.idx >= c:
                self.idx -= c
                self.row += 1


class GridColumnInserter(GridInserter):
    """
    Inserts items into a column in the grid.
    """


    def __init__(self, grid, column = 0, automatically_to_next_column = False):
        GridInserter.__init__(self, grid)
        self.idx = column
        self.row = 0
        self.automatically_to_next_column = automatically_to_next_column

    def add_child(self, child):
        if self.automatically_to_next_column and self.row >= \
                self.grid.get_rows():
            self.idx += 1
            self.row = 0

        assert self.idx < self.grid.get_columns()
        assert self.row < self.grid.get_rows()

        if child:
            self.grid.add_child(child, self.idx, self.row)

        self.row += 1

    def skip(self, count):
        assert self.row < self.grid.get_rows()
        self.row += count
        if self.automatically_to_next_column:
            r = self.grid.get_rows()
            assert r > 0
            while self.row >= r:
                self.row -= c
                self.idx += 1


_panners = {}
def _panner_callback(event):
    n = event.get_event_name()
    c = event.component

    if n == "StartPanEvent":
        oldpos = c.get_position()
        x = event.x - oldpos[0]
        y = event.y - oldpos[1]
        _panners[c] = (x, y)

    elif n == "DoPanEvent":
        oc = _panners[c]
        c.set_position(event.x - oc[0],
                       event.y - oc[1])

    elif n == "EndPanEvent":
        oc = _panners[c]
        c.set_position(event.x - oc[0],
                       event.y - oc[1])
        del _panners[c]

    else:
        assert 0

def _add_panner_to_component(component):
    component.signal_pan.set_enabled(True)
    component.signal_pan.add(_panner_callback)
