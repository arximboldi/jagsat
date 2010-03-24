#
# This file is copyright Tribeflame Oy, 2009.
#
import sys
import math
import inspect
import traceback

from PySFML import sf
from tf.gfx.imagefile import ImageFile
from tf.behavior import gameloop
from tf import signalslot

__all__ = [
'NORTH',
'WEST',
'SOUTH',
'EAST',
'CENTER'
'NORTHEAST',
'SOUTHEAST',
'SOUTHWEST',
'NORTHWEST',
'Color',
'Transparent'
'Window',
'View',
'Layer'
#'Space',
'HitShape',
'Component',
'Image',
'FreeformContainer',
'OrganizedContainer',
'VBox',
'HBox',
'Grid',
'BigImage',
'String',
'i18nString',
'MultiLineString',
'i18nMultiLineString',
'Line',
'Circle',
'Rectangle',
'RoundedRectangle']

NORTH = (0.5, 0.0)
WEST = (0.0, 0.5)
SOUTH = (0.5, 1.0)
EAST = (1.0, 0.5)

CENTER = (0.5, 0.5)

NORTHEAST = (1.0, 0.0)
SOUTHEAST = (1.0, 1.0)
SOUTHWEST = (0.0, 1.0)
NORTHWEST = (0.0, 0.0)

from OpenGL.GL import *
from OpenGL.GLU import *


Color = sf.Color
Transparent = sf.Color(255, 0, 255, 0)


class Window:
    """The main window that contains views."""

    def __init__(self, sfwindow):
        """
        Wrap a window into the TF system.

        @sfwindow - An SFML RenderWindow object as parameter.
        """
        self.window = sfwindow
        self.views = []

    def add_view(self, view):
        """
        Add a @View to the window.
        """
        #assert isinstance(view, View)
        self.views.append(view)

    def clear(self, color):
        """
        Clear the screen and depth buffer.

        This should only be needed in the eventloop.
        """
        self.window.Clear(color)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


class View:
    """
    A View is a container of @Layer objects. The view can be seen as a camera,
    which can recenter itself and its zoom e.g. on a game board map.

    Signals:

    signal_zoom_change
        Called when the zoom changes.
        Event info:
        view - this View object
        zoom - the zoom value
        centerx - the center coordinate horizontally
        centery - the center coordinate vertically

    signal_position - Called when the position changes.

    """

    def __init__(self, window, sfview):
        print window
        print window.__class__
        print "W", Window
        assert isinstance(window, Window)
        self.window = window
        self.view = sfview
        self.layers = []
        self.window.add_view(self)
        self.viewfocus = None
        self.minzoom = 0.5
        self.maxzoom = 2.0
        self.zoom = 1.0
        self.signal_zoom_change = signalslot.Signal("zoom_change")
        self.signal_position = signalslot.Signal("position_change")
        self.content_width = 0
        self.content_height = 0

    def get_zoom(self):
        return self.zoom

    def get_zoom_min(self):
        return self.minzoom

    def get_zoom_max(self):
        return self.maxzoom

    def set_zoom_min(self, z):
        self.minzoom = z

    def set_zoom_max(self, z):
        self.maxzoom = z

    def set_zoom(self, newzoom):
        if newzoom > self.maxzoom:
            newzoom = self.maxzoom
        elif newzoom < self.minzoom:
            newzoom = self.minzoom
        if self.zoom != newzoom:
            self.zoom = newzoom
            cx, cy = self.view.GetCenter()
            self.signal_zoom_change.call(signalslot.Event("ZoomChangeEvent",
                                                          view = self,
                                                          zoom = self.zoom,
                                                          centerx = cx,
                                                          centery = cy))
            self._fix_zoom()

    def set_zoom_rel(self, rel):
        self.set_zoom(self.zoom + rel)

    def _fix_zoom(self):
        w = self.get_window().window
        h = w.GetHeight() / 2.0
        w = w.GetWidth() / 2.0
        self.view.SetHalfSize(w / self.zoom,
                              h / self.zoom)
        self.recenter_view_rel(0, 0)

    def recenter_view_rel(self, dx, dy):
        cntr = self.view.GetCenter()
        ncx = cntr[0] + dx
        ncy = cntr[1] + dy
        self.recenter_view(ncx, ncy)

    def recenter_view(self, cx, cy):
        cntr = self.view.GetCenter()
        h = self.view.GetHalfSize()
        hx = h[0]
        hy = h[1]
        if cx - hx < 0:
            cx += -(cx-hx)
        if cy - hy < 0:
            cy += -(cy-hy)
        if cx + hx > self.content_width:
            cx += self.content_width-(cx+hx)
        if cy + hy > self.content_height:
            cy += self.content_height-(cy+hy)

        if cx == cntr[0] and cy == cntr[1]:
            return
        self.view.SetCenter(cx, cy)
        e = signalslot.Event("PositionChange",
                             zoom = self.zoom,
                             centerx = cx,
                             centery = cy)
        self.signal_position.call(e)

    def set_view_focus(self, vf):
        vf.view = self
        self.viewfocus = vf
        self.viewfocus.start()

    def get_view_focus(self):
        return self.viewfocus

    def get_window(self):
        return self.window

    def add_layer(self, lr):
        assert lr not in self.layers
        self.layers.append(lr)
        lr._view = self

    def remove_layer(self, lr):
        assert lr in self.layers
        self.layers.remove(lr)
        lr._view = None

    def tick(self, gameloop):
        if self.viewfocus:
            self.viewfocus.tick()

    def draw(self, window):
        window.window.SetView(self.view)
        ordered = order_layers (self.layers)
        for i, lr in ordered:
            lr.draw(window.window)


class Layer:
    """
    A Layer object contains a set of user interface components (sprites,
    animations) that are going to be drawn. Note that a Layer is not a
    user interface component, but primarily a means to group
    components according to their z-order. Because of this, the interface is
    also severely restricted.
    """

    def __init__(self, _view):
        self._visible = True
        self.objects = []
        #assert isinstance(_view, View)
        self._view = _view
        self._view.add_layer(self)
        self.zorder = 0
        
    def set_visible(self, is_visible):
        v = self._visible
        self._visible = is_visible
        return v

    def get_visible(self):
        return self._visible

    def get_view(self):
        return self._view

    def get_window(self):
        return self._view.get_window()

    #def rearrange_objects(self):
    #    self.objects.sort(lambda a, b: cmp(a.y, b.y))

    def draw(self, window):
        if not self._visible:
            return

        for o in self.objects:
            o.draw(window)

    def add_object(self, obj):
        assert obj
        assert obj not in self.objects
        if not hasattr(obj, "draw"):
            print "tiloc: ERROR, you are drawing a", obj, \
                ", this is possibly a PySFML native object."
        self.objects.append(obj)
        assert obj._layer is None
        obj._layer = self

    add_child = add_object

    def remove_object(self, obj):
        assert obj
        assert obj in self.objects
        self.objects.remove(obj)
        obj._layer = None
        obj.remove_myself()

    remove_child = remove_object

def order_layers (layers):
    return sorted (enumerate (layers),
                   lambda (i, x), (j, y):
                   cmp (x.zorder, y.zorder) or cmp (i, j))

class Space:

    def __init__(self):
        self.set_padding(0)
        self.set_margin(0)

    def set_padding(self, p1, p2 = None, p3 = None, p4 = None):
        if p2 is None:
            p2 = p1
        if p3 is None:
            p3 = p1
        if p4 is None:
            p4 = p2

        if p1 is not None:
            self.padding_top = p1
        if p2 is not None:
            self.padding_right = p2
        if p3 is not None:
            self.padding_bottom = p3
        if p4 is not None:
            self.padding_left = p4
        self._recalculate_parent_chain()

    def set_margin(self, m1, m2 = None, m3 = None, m4 = None):
        if m2 is None:
            m2 = m1
        if m3 is None:
            m3 = m1
        if m4 is None:
            m4 = m2

        if m1 is not None:
            self.margin_top = m1
        if m2 is not None:
            self.margin_right = m2
        if m3 is not None:
            self.margin_bottom = m3
        if m4 is not None:
            self.margin_left = m4
        self._recalculate_parent_chain()


class HitShape:
    """The HitShape class defines how objects can be hit. By default,
    a simple rectangular shape is assumed.

    This is used by the Component class, and by tf.gfx.uihelp.hit_sprite.
    """

    # The shape of the object is a rectangle (or a square, if width
    # equals height)
    RECTANGLE = 0

    # The shape of the object is an ellipse (or a circle, if width
    # equals height)
    ELLIPSE = 1

    # The shape is defined by the alpha channel, where the alpha
    # (opacity) must be over 50% (i.e. >= 128)
    NONALPHA = 2

    # This shape is defined by the is_hit() member function, which
    # should be overriden. Note: It should be rather fast!
    USERDEFINED = 3

    def __init__(self, shape = RECTANGLE):
        self.shape = shape

    def get_hit_shape(self):
        return self.shape

    def set_hit_shape(self, shape):
        self.shape = shape

    def is_hit(self, x, y):
        """
        Override this when using HitShape.USERDEFINED. The x and y coordinates
        are local.
        """
        raise NotImplemented("You must override the is_hit() function when" + \
                                 " using HitShape.USERDEFINED!")


class Component(sf.Drawable, Space, HitShape):

    # sf compatibility
    get_position = sf.Drawable.GetPosition
    set_rotation = sf.Drawable.SetRotation
    get_rotation = sf.Drawable.GetRotation
    get_scale = sf.Drawable.GetScale
    set_scale = sf.Drawable.SetScale
    # SetColor = None
    # BUG add more

    def set_color(self, c):
        return self._sprite.SetColor(c)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        n = ""
        if hasattr(self, "name"):
            n = " \"" + str(self.name) + "\""
        pos = self.GetPosition()
        s = "<%s%s (%d, %d) at %X>" % (self.__class__.__name__, n,
                                       pos[0], pos[1], id(self))
        return s

    # CHILD HANDLING

    def _recalculate_parent_chain(self):
        """
        Sets @self and parent chain to recalculate their dimensions.
        Detects loop using standard trick.
        """
        # BUG there are many other cases where this should be recalculated?
        self._recalculate_displaylist()

        p = self
        p2 = self
        every_2nd = True
        while p:
            assert p
            assert p2
            if p._need_to_recalculate:
                break
            p._need_to_recalculate = True
            p = p.parent
            if p and p2 and p == p2:
                print "tf: Error, child loop detected!"
                while True:
                    print "tf component:", p
                    p = p.parent
                    assert p
                    if p == p2:
                        break
                assert 0
            every_2nd = every_2nd ^ True
            if every_2nd:
                p2 = p2.parent

    def _add_child_somewhere(self, lst, obj, after, before):
        assert obj not in lst
        assert obj != self
        if obj._layer:
            obj._layer.remove_object(obj)
        if obj.parent:
            obj.parent.remove_child(obj)
        if before:
            assert after is None
            idx = lst.index(before)
            lst.insert(idx, obj)
        elif after:
            assert before is None
            idx = lst.index(after)
            lst.insert(idx+1, obj)
        else:
            lst.append(obj)
        obj.parent = self
        obj._recalculate_parent_chain()

    def add_child(self, obj, after=None, before=None):
        self._add_child_somewhere(self.children, obj, after, before)

    def add_back_child(self, obj, after=None, before=None):
        self._add_child_somewhere(self.children_back, obj, after, before)

    def remove_child(self, obj):
        assert obj != self
        if obj in self.children:
            self.children.remove(obj)
        elif obj in self.children_back:
            self.children_back.remove(obj)
        else:
            assert 0
        obj.parent = None
        obj.remove_myself()
        self._recalculate_parent_chain()

    def get_child(self, idx):
        return self.children[idx]

    def get_back_child(self, idx):
        return self.children_back[idx]

    def remove_myself(self):
        """
        Equivalent to killing the object. It, or its children, can no
        longer be used.  Its actions are stopped immediately.
        """
        # BUG also go through children
        if self._displaylist_number != -1:
            print "Deleting display list", self._displaylist_number
            glDeleteLists(self._displaylist_number, 1)
            self._displaylist_number = -1
        if self._layer:
            self._layer.remove_object(self)
        if self.parent:
            self.parent.remove_child(self)
        if len(self._keyboard_shortcuts) != 0:
            g = gameloop.get_game_loop()
            km = g.get_keyboardmanager()
            # Need a copy here
            for k, func in list(self._keyboard_shortcuts):
                km.remove_keyboard_shortcut(self,
                                            k,
                                            func)
            assert len(self._keyboard_shortcuts) == 0

        self.remove_all_actions()

    # INIT

    def __init__(self, parent = None):
        sf.Drawable.__init__(self)
        self.parent = None
        self._layer = None
        self.children = []
        self.children_back = []

        self._displaylist_p = False
        self._displaylist_number = -1

        self._need_to_recalculate = True
        self._keyboard_shortcuts = []
        Space.__init__(self)
        HitShape.__init__(self, HitShape.RECTANGLE)

        if parent:
            # Can be layer, another uicomponent
            # or an inserter
            parent.add_child(self)

        # If this is false, the user can't press it.
        self._enable_hitting = False
        self.signal_click = signalslot.Signal("Click")
        self.signal_click.set_enabled(False)

        # This receives start, pan, stop events.
        self.signal_pan = signalslot.Signal("Pan")
        self.signal_pan.set_enabled(False)

        # If this is false, the user can't see it.
        # XXX does it take space in containers?
        self._visible = True

        self._expand_as_necessary_x = False
        self._expand_as_necessary_y = False

        s = id(self)
        try:
            s = str(self)
        except:
            pass
#        print "Created", s
#
#        try:
#            assert 0
#        except:
#            traceback.print_stack(file=sys.stdout)

#    def __del__(self):
#        self.kill()
#
#    def kill(self):
#        self.remove_myself()
#        self.active_actions.clear()
#        self.actions.clear()

    def _recalculate_displaylist(self):
        if self._displaylist_p is False:
            p = self.get_parent()
            if p:
                p._recalculate_displaylist()
            return

        if self._displaylist_number >= 0:
#            print "Deleting display list", self._displaylist_number
            glDeleteLists(self._displaylist_number, 1)
        self._displaylist_number = -1

    def set_displaylist(self, p):
        self._displaylist_p = p
        if not p:
            self._recalculate_displaylist()

    def set_visible(self, is_visible):
        v = self._visible
        self._visible = is_visible
        self._recalculate_parent_chain()
        return v

    def get_visible(self):
        return self._visible

    def get_parent(self):
        return self.parent

    def set_parent(self, p):
        if not p:
            self.remove_myself()
            return
        p.add_child(self)

    def get_layer(self):
        p = self
        while p:
            if p._layer:
                return p._layer
            p = p.parent
        return None

    def get_view(self):
        l = self.get_layer()
        if not l:
            return None
        return l.get_view()

    def get_window(self):
        v = self.get_view()
        if not v:
            return None
        return v.get_window()

    def set_enable_hitting(self, enable):
        self._enable_hitting = enable
        self.signal_click.set_enabled(enable)

    def get_enable_hitting(self):
        return self.signal_click.is_enabled()

    # ACTIONS

    def get_active_actions(self):
        gl = gameloop.get_game_loop()
        return gl._actionmanager.get_active_actions(self)

    def add_action(self, action, wait_for = None):
        """
        Add @action and start it, unless @wait_for specifies some
        other action.
        """
        assert action is not None
        gl = gameloop.get_game_loop()
        gl._actionmanager.add_action(self, action, wait_for)

    def add_action_sequence(self, actions):
        if not actions:
            return
        prev = actions[0].waiting_for
        for act in actions:
            if act:
                self.add_action(act, prev)
                prev = act

    def add_parallell_actions(self, *args):
        for act in args:
            self.add_action(act)

    def remove_all_actions(self):
        gl = gameloop.get_game_loop()
        gl._actionmanager.remove_all_actions(self)

    def remove_all_actions_of_type(self, type):
        gl = gameloop.get_game_loop()
        gl._actionmanager.remove_actions(self,
                                         lambda x: isinstance(x, type))

    def user_hit(self, gameloop, localx, localy):
        """
        Called when user hits the component, and set_enabled_hit(True)
        has been called.

        You probably should not override this, and instead just hook
        into the signal_click signal instead. See tf.signalslot for
        details.
        """
        self.signal_click.call(signalslot.Event("ClickEvent",
                                                component = self,
                                                x = localx,
                                                y = localy))

    def set_expand(self, xexpandp, yexpandp):
        self._expand_as_necessary_x = xexpandp
        self._expand_as_necessary_y = yexpandp
        self._recalculate_parent_chain()

    def set_expand_x(self, xexpandp):
        self._expand_as_necessary_x = xexpandp
        self._recalculate_parent_chain()

    def set_expand_y(self, yexpandp):
        self._expand_as_necessary_y = yexpandp
        self._recalculate_parent_chain()

    def get_expand(self):
        return (self._expand_as_necessary_x,
                self._expand_as_necessary_y)

    def get_expand_x(self):
        return self._expand_as_necessary_x

    def get_expand_y(self):
        return self._expand_as_necessary_y


# OBSOLETE - DO NOT USE
#    def start_pan(self, event):
#        pass
#
#    def do_pan(self, event):
#        pass
#
#    def end_pan(self, event):
#        pass

    def _do_recalculate(self, window):
        self._do_set_center()

    def _fix_recalculating(self, window):
        if self._need_to_recalculate:
            #print "recalculating", self
            self._need_to_recalculate = False
            for child in self.children_back:
                child._fix_recalculating(window)
            for child in self.children:
                child._fix_recalculating(window)
            self._do_recalculate(window)

    def draw(self, window):
        """Draws sprite on screen."""
        # The check is here for a small speed increase
        if self._need_to_recalculate:
            self._fix_recalculating(window)
        # Check here instead of in self.Render,
        # so that the transformation matrix does not have to be set.
        if not self._visible:
            return
        # This just calls self.Render,
        # after setting up the transformation matrix
        window.Draw(self)

    def Render(self, window):
        """@internal. Called indirectly from self.draw."""

        if self._displaylist_p:
            if self._displaylist_number == -1:
                # This will cause us to bind all the textures once.
                #
                # By binding all the required textures, we ensure
                # that the texture is in fact generated by SFML
                # and it is sent to the gpu. Note that this must be done
                # outside of the display list creation, otherwise things
                # slow down considerably.
                pass
            elif self._displaylist_number == -2:
                self._displaylist_number = glGenLists(1)
#                print "Creating display list", \
#                       self._displaylist_number, "for", self
                glNewList(self._displaylist_number, GL_COMPILE_AND_EXECUTE)
            else:
                #print "Calling list", self._displaylist_number
                glCallList(self._displaylist_number)
                return

        # Draw first the back children.
        # Draw them inside @self, so that its transformation matrix
        # is used.
        for c in self.children_back:
            c.draw(window)

        # Draw @self
        if self._sprite is not None:
            window.Draw(self._sprite)

        # Now draw the "ordinary" children.
        # Draw children inside @self, so that its transformation matrix
        # is used.
        for c in self.children:
            c.draw(window)

        if self._displaylist_p:
            if self._displaylist_number == -1:
                self._displaylist_number = -2
            elif self._displaylist_number > 0:
                glEndList()

    def _get_width(self):
        # BUG? Does not take parent chain into account?
        return self._get_unscaled_width() * self.GetScale()[0] \
            + self.padding_left + self.padding_right

    def _get_height(self):
        # BUG? Does not take parent chain into account?
        return self._get_unscaled_height() * self.GetScale()[1] \
            + self.padding_top + self.padding_bottom

    def _get_unscaled_width(self):
        raise NotImplemented

    def _get_unscaled_height(self):
        raise NotImplemented

    def resize(self, nx, ny):
        sx = nx / float(self._get_unscaled_width())
        sy = ny / float(self._get_unscaled_height())
        self.SetScale(sx, sy)

    # SPRITE CENTER

    def _do_set_center(self):
        if hasattr(self, "center_px"):
            # The +0.5 is for placing images with
            # odd sizes at exactly the center
            self.SetCenter(\
                int(self._get_unscaled_width() * self.center_px + 0.5),
                int(self._get_unscaled_height() * self.center_py + 0.5))
        elif hasattr(self, "center_cx"):
            self.SetCenter(self.center_cx, self.center_cy)

    def set_center(self, x, y = None):
        """Set the center coordinates of the sprite, in absolute pixels."""
        if y is None:
            x, y = x
        self.center_cx = x
        self.center_cy = y
        if hasattr(self, "center_px"):
            del self.center_px
            del self.center_py
        self._do_set_center()

    def set_center_rel(self, center_px, center_py = None):
        """
        Set the center coordinates of the sprite, relative to the size
        of the image.  Thus, the values given are usually between 0.0
        and 1.0.
        """
        if center_py is None:
            center_px, center_py = center_px
        self.center_px = center_px
        self.center_py = center_py
        if hasattr(self, "center_cx"):
            del self.center_cx
            del self.center_cy
        self._do_set_center()

    # SPRITE POSITION

    def set_position(self, x, y = None):
        """Set the position coordinates of the sprite, in absolute pixels."""
        if y is None:
            x, y = x
        self.SetPosition(x, y)

    def set_position_delta(self, dx, dy = None):
        """Move the position coordinates of the sprite, in absolute pixels."""
        if dy is None:
            dx, dy = dx
        self.Move(dx, dy)

    def set_position_rel(self, position_px, position_py = None):
        """
        Set the position coordinates of the sprite, relative to the
        size of the ***window***.  Thus, the values given are usually
        between 0.0 and 1.0.

        NOTE: WTF?! TO THE SIZE OF THE WINDOW OR THE PARENT? THIS SUCKS!
        """
        if position_py is None:
            position_px, position_py = position_px

        if self.parent:
            x = int(self.parent._get_unscaled_width() * position_px)
            y = int(self.parent._get_unscaled_height() * position_py)
            self.SetPosition(x, y)
        elif self._layer:
            window = self._layer.get_window()
            x = int(window.window.GetWidth() * position_px)
            y = int(window.window.GetHeight() * position_py)
            self.SetPosition(x, y)
        else:
            print "tf: Warning, calling set_position_rel without any effect."

    def _do_image_updated(self, image):
        self._recalculate_parent_chain()

    def activate(self):
        """
        Activation methods for more advanced GUI stuff.

        Largely unused currently.
        """
        for x in self.children: x.activate ()

    def deactivate(self):
        for x in self.children: x.deactivate ()



class Image(Component):

    def __init__(self, parent = None, fname = None):
        Component.__init__(self, parent)
        if fname is not None:
            self.img = ImageFile.new_image(fname)
        else:
            self.img = ImageFile.empty_image
        self._sprite = sf.Sprite(self.img.img)

    def load_image (self, fname):
        self.set_image (ImageFile.new_image (fname))

    def set_image(self, img):
        self.img = img
        self._sprite.SetImage(self.img.img)
        i = sf.IntRect(0,
                       0,
                       self.img.img.GetWidth(),
                       self.img.img.GetHeight())
        self._sprite.SetSubRect(i)
        self._recalculate_parent_chain()

    def get_image(self):
        return self.img

    def _get_unscaled_width(self):
        return self.img.img.GetWidth()

    def _get_unscaled_height(self):
        return self.img.img.GetHeight()

    def __repr__(self):
        n = ""
        if hasattr(self, "name"):
            n = " \"" + str(self.name) + "\""
        pos = self.GetPosition()
        if hasattr(self, "img") and self.img:
            fname = self.img.filename
        else:
            fname = "Unknown file"
        s = "<%s%s of %s (%d, %d) at %X>" % (self.__class__.__name__, n,
                                             fname,
                                             pos[0], pos[1], id(self))
        return s


class FreeformContainer(Component):

    def __init__(self, parent = None):
        Component.__init__(self, parent)
        # XXX these are important when checking for hits
        self.width = 0
        self.height = 0
        # This is here to avoid hasattr; a small speed increase
        self._sprite = None

    def _get_unscaled_width(self):
        return self.width

    def _get_unscaled_height(self):
        return self.height


class OrganizedContainer(Component):

    def __init__(self, parent = None):
        Component.__init__(self, parent)
        # This is here to avoid hasattr; a small speed increase
        self._sprite = None


class VBox(OrganizedContainer):

    def __init__(self, parent = None, center = False):
        OrganizedContainer.__init__(self, parent)
        self.center_childs = center
        self.separation = 0
        
    def _do_recalculate(self, window):
        OrganizedContainer._do_recalculate(self, window)

        x, y = 0, 0
        # x, y = self.GetPosition ()
        # x = x / 2 + self.margin_left + self.padding_left
        # y = y / 2 + self.margin_top + self.padding_top

        width = self._get_width ()
        for child in self.children:
            #if not child._visible:
            #    continue
            if self.center_childs:
                x = (width - child._get_width ()) / 2
            child.SetPosition(x + child.padding_left,
                              y + child.padding_top)
            y += self.padding_top + self.padding_bottom + self.separation
            y += child._get_height()

    def _get_unscaled_width(self):
        w = 0
        for child in self.children:
            #if child._visible:
            w = max(w, child._get_width())
        return w + self.margin_left + self.margin_right + \
            self.padding_left + self.padding_right

    def _get_unscaled_height(self):
        h = self.margin_top + self.margin_bottom
        for child in self.children:
            #if not child._visible:
            #    continue
            h += child._get_height()
            h += self.padding_top + self.padding_bottom + self.separation
        return h


class HBox(OrganizedContainer):

    def __init__(self, parent = None, center = False):
        OrganizedContainer.__init__(self, parent)
        self.center_childs = center
        self.separation = 0
        
    def _do_recalculate(self, window):
        OrganizedContainer._do_recalculate(self, window)

        x, y = 0, 0
        height = self._get_height ()
        
        for child in self.children:
            #if not child._visible:
            #    continue
            if self.center_childs:
                y = (height - child._get_height ()) / 2
            child.SetPosition (x + child.padding_left,
                               y + child.padding_top)
            x += self.padding_left + self.padding_right + self.separation
            x += child._get_width ()

    def _get_unscaled_width(self):
        w = self.margin_left + self.margin_right
        for child in self.children:
            #if not child._visible:
            #    continue
            w += child._get_width()
            w += self.padding_left + self.padding_right + self.separation
        return w

    def _get_unscaled_height(self):
        h = 0
        for child in self.children:
            #if child._visible:
            h = max(h, child._get_height())
        return h + self.margin_top + self.margin_bottom + self.padding_top + \
            self.padding_bottom


class Grid(OrganizedContainer):

    def __init__(self, parent = None, gridwidth = 3, gridheight = 3):
        OrganizedContainer.__init__(self, parent)
        self.width = 0
        self.height = 0
        self._need_to_recalculate = True
        self.children_grid = []
        # NOTE, self.children contains the children in an arbitrary order!
        for i in range(gridheight):
            w = [None] * gridwidth
            self.children_grid.append(w)

        # not used yet
        self.offsets_x = [0] * gridwidth
        self.offsets_y = [0] * gridheight

    def get_columns(self):
        return len(self.children_grid[0])

    def get_rows(self):
        return len(self.children_grid)

    def set_visible_row(self, visible, row):
        for child in self.children_grid[row]:
            child.set_visible(visible)

    def set_visible_column(self, visible, column):
        for child_row in self.children_grid:
            child_row[column].set_visible(False)

    def _fix_recalculating(self, window):
        if self._need_to_recalculate:
            self._need_to_recalculate = False
            for child in self.children_back:
                child._fix_recalculating(window)
            for child_grid in self.children_grid:
                for child in child_grid:
                    if child:
                        child._fix_recalculating(window)
            self._do_recalculate(window)

    def add_child(self, child, x, y):
        c = self.children_grid[y][x]
        if c:
            c.remove_myself()
        # BUG _layer
        child.remove_myself()
        self.children_grid[y][x] = child
        OrganizedContainer.add_child(self, child)

    def remove_child(self, child_to_remove):
        OrganizedContainer.remove_child(self, child_to_remove)
        for child_grid in self.children_grid:
            for child in child_grid:
                if child is child_to_remove:
                    child_grid.remove(child)
                    return

    def get_child(self, x, y):
        c = self.children_grid[y][x]
        return c

    def _do_recalculate(self, window):
        self.width = self._slow_get_width()
        self.height = self._slow_get_height()
        OrganizedContainer._do_recalculate(self, window)

        origx = self.margin_left
        y = self.margin_top
        for idx_y, child_grid in enumerate(self.children_grid):
            x = origx
            for idx_x, child in enumerate(child_grid):
                if child and child._visible:
                    child.SetPosition(x, y)
                x += self.offsets_x[idx_x]
                #x += self.padding_right + self.padding_left
            y += self.padding_top + self.padding_bottom
            y += self.offsets_y[idx_y]

    def draw(self, window):
        if not self._visible:
            return
        window.Draw(self)

    def Render(self, window):
        """@internal."""
        #window.Draw(self._sprite)
        for child_grid in self.children_grid:
            for child in child_grid:
                if child and child._visible:
                    window.Draw(child)

    def _get_unscaled_width(self):
        return self.width

    def _get_unscaled_height(self):
        return self.height

    def _slow_get_width(self):
        maxw = 0
        for idx_y, child_grid in enumerate(self.children_grid):
            maxh = 0
            #w = -self.padding_left - self.padding_right
            w = 0
            for child in child_grid:
                if child and child._visible:
                    w += child._get_width()
                    maxh = max(maxh, child._get_height() + self.padding_top + \
                                   self.padding_bottom)
                w += self.padding_left + self.padding_right
            maxw = max(maxw, w)
            self.offsets_y[idx_y] = maxh - self.padding_top
        maxw += self.margin_left + self.margin_right
        return maxw

    def _slow_get_height(self):
        maxh = 0
        for idx_x in range(len(self.children_grid[0])):
            #h = -self.padding_top - self.padding_bottom
            h = 0
            maxw = 0
            for idx_y in range(len(self.children_grid)):
                child = self.children_grid[idx_y][idx_x]
                if child and child._visible:
                    h += child._get_height()
                    maxw = max(maxw, child._get_width() + self.padding_left + \
                                   self.padding_right)
                h += self.padding_top + self.padding_bottom
            maxh = max(maxh, h)
            self.offsets_x[idx_x] = maxw - self.padding_left
        maxh += self.margin_top + self.margin_bottom
        return maxh


class BigImage(Component):
    """
    BUG probably doesn't work at all with x,y coord changes etc.
    """

    def __init__(self, parent, fname, width_in_images):
        Component.__init__(self)
        self.images = []
        self._sprites = []
        self.width_in_images = width_in_images
        self.maxwidth = 0
        self.maxheight = 0
        i = 0
        while True:
            try:
                img = ImageFile.new_image(fname % i)
            except:
                print sys.exc_value
                break
            self.images.append(img)
            i += 1
        if i == 0:
            print "tf: Could not find", fname, "bigimage, error!"
            assert i > 0
        i = 0
        for i, img in enumerate(self.images):
            self._sprites.append(sf.Sprite(img.img))
        self.reposition()

    def reposition(self):
        x = 0
        y = 0
        i = 0
        for idx, s in enumerate(self._sprites):
            img = self.images[idx]
            s.SetPosition(x, y)
            x += img.img.GetWidth()
            idx += 1
            i += 1
            if i >= self.width_in_images:
                i = 0
                y += img.img.GetHeight()
                x = 0
        self.maxwidth = sum([i.img.GetWidth() \
                                 for i in \
                                 self.images[0:self.width_in_images]])
        self.maxheight = y

    def _is_visible(self, view, s):
        sx, sy = s.GetPosition()
        sw, sh = s.GetSize()

        vcx, vcy = view.view.GetCenter()
        vhx, vhy = view.view.GetHalfSize()

        # BUG only works if @s is untransformed
        ### assert hasattr(s, "_layer")

        if sx > vcx + vhx:
            return False
        if sx + sw < vcx - vhx:
            return False

        if sy > vcy + vhy:
            return False
        if sy + sh < vcy - vhy:
            return False

        return True

    def Render(self, window):
        """@internal."""
        assert self._displaylist_p is False

        for c in self.children_back:
            c.draw(window)
        view = self.get_view()
        for s in self._sprites:
            # XXX We use a displaylist, so no need to check
            # No we do not use one
            #if self._is_visible(view, s):
            window.Draw(s)

        for c in self.children:
            window.Draw(c)

    def _get_unscaled_width(self):
        return self.maxwidth

    def _get_unscaled_height(self):
        return self.maxheight


class String(Component):

    def __init__(self, parent = None, string = u"", *args, **kwargs):
        if not isinstance(string, unicode):
            raise TypeError("tf: Error: String " + string + " is not unicode.")
        Component.__init__(self, parent)
        self._sprite = sf.String(string, *args, **kwargs)
        self._string = string
        self._recheck_size ()
        # XXX would be nice to set the displaylist for strings

    def _recheck_size (self):
        string = self._string
        
        if string and string [0] == "%":
            print "checking string: ", string
            idx   = string [1:].find ('%')
            if idx >= 0:
                size  = int (string [1:idx+1])
                txt   = string [idx+2:]
                print size, txt
                self._sprite.SetSize (size)
                self._sprite.SetText (txt)
    
    def __repr__(self):
        n = ""
        if hasattr(self, "name"):
            n = " \"" + str(self.name) + "\""
        pos = self.GetPosition()
        stringval = self._sprite.GetText().encode("UTF-8")
        s = "<%s%s \"%s\" (%d, %d) at %X>" % (self.__class__.__name__, n,
                                              stringval,
                                              pos[0], pos[1], id(self))
        return s

    def set_size(self, size):
        ret = self._sprite.SetSize(size)
        self._recheck_size ()
        return ret
    
    def set_string(self, string):
        #assert isinstance(string, unicode)
        self._string = string
        self._sprite.SetText(string)
        self._recheck_size ()
        self._recalculate_parent_chain()

    def get_string(self):
        s = self._sprite.GetText()
        #assert isinstance(s, unicode)
        return s

    def _get_unscaled_width(self):
        return self._sprite.GetRect().GetWidth()

    def _get_unscaled_height(self):
        if len (self._string) < 1: return 0
        return self._sprite.GetSize()


class i18nString(String):

    def __init__(self, parent, lcn, key, *args, **kwargs):
        if not key:
            print "tf: Error: i18nstring should have key!"
            assert 0
        assert isinstance(key, str)
        # use key temporarily
        String.__init__(self, parent, unicode(key, "ascii"), *args, **kwargs)
        self.key = key
        self.lcn = lcn # This isn't really needed.
        self.lcn._register_for_language_change(self)

    def get_key(self):
        return self.key

    def get_language_change_notifier(self):
        return self.lcn


class MultiLineString(VBox):

    def __init__(self, parent = None, strings = None, center=False,
                 *args, **kwargs):
        if strings is not None:
            for s in strings:
                assert isinstance(s, unicode)

        VBox.__init__(self, parent, center=center)
        self.args = args
        self.kwargs = kwargs
        if isinstance(strings, unicode):
            self.set_string(strings, *args, **kwargs)
            return

        self.set_strings(strings, *args, **kwargs)

    def set_color(self, c):
        for i in self.children:
            i.set_color(c)

    def set_font(self, f):
        for i in self.children:
            i._sprite.SetFont(f)

    def set_size(self, size):
        for i in self.children:
            i.set_size(size)

    def set_string(self, string, *args, **kwargs):
        if string is None:
            self.set_strings(None, *args, **kwargs)
            return
        assert isinstance(string, unicode)
        self.set_strings(string.split("\n"), *args, **kwargs)

    def set_strings(self, strings, *args, **kwargs):
        if strings is not None:
            ll = len(strings)
            for s in strings:
                assert isinstance(s, unicode)
        else:
            ll = 0
        while len(self.children) > ll:
            self.children[-1].remove_myself()

        if not args:
            args = self.args
        if not kwargs:
            kwargs = self.kwargs
        if strings is not None:
            for idx, str in enumerate(strings):
                if idx >= len(self.children):
                    line = String(u"", *args, **kwargs)
                    self.add_child(line)
                self.children[idx].set_string(str)
        self._recalculate_parent_chain()


class i18nMultiLineString(MultiLineString):

    def __init__(self, parent, lcn, key, *args, **kwargs):
        if not key:
            print "tf: Error: i18nstring should have key!"
            assert 0
        assert isinstance(key, str)
        # use key temporarily
        MultiLineString.__init__(self,
                                 parent,
                                 unicode(key, "ascii"),
                                 *args,
                                 **kwargs)
        self.key = key
        self.lcn = lcn # This isn't really needed.
        self.lcn._register_for_language_change(self)

    def get_key(self):
        return self.key

    def get_language_change_notifier(self):
        return self.lcn


class Line(Component):

    def __init__(self, parent, x1, y1, x2, y2,
                 it, ic, ot, oc):
        Component.__init__(self, parent)
        self._sprite = sf.Shape.Line(x1, y1, x2, y2, it, ic, ot, oc)

    def _get_unscaled_width(self):
        return 0

    def _get_unscaled_height(self):
        return 0


class Circle(Component):

    def __init__(self,
                 parent = None,
                 radius = 10,
                 ic = sf.Color (0, 0, 0),
                 ot = 2.0,
                 oc = sf.Color (255, 255, 255)):
        assert parent
        Component.__init__(self, parent)
        x = radius
        y = radius
        self._sprite = sf.Shape.Circle(x, y, radius, ic, ot, oc)
        self._width = radius * 2
        self._height = radius * 2
    
    def _get_unscaled_width(self):
        return self._width

    def _get_unscaled_height(self):
        return self._height


class Rectangle(Component):

    def __init__(self, parent, x1, y1, w, h,
                 ic, oc, ot):
        Component.__init__(self, parent)
        x2 = x1 + w
        y2 = y1 + h
        self._sprite = sf.Shape.Rectangle(x1, y1, x2, y2, ic, ot, oc)
        self._width = w
        self._height = h
        self._ot = ot
        
    def set_color (self, c):
        x1, y1 = self.get_position ()
        x2, y2 = x1 + self._width, y1 + self._height
        self._sprite = sf.Shape.Rectangle(x1, y1, x2, y2, c, self._ot, c)

    def _get_unscaled_width(self):
        return self._width

    def _get_unscaled_height(self):
        return self._height


def get_bounding_box_for_children(children):
    sx = 0
    sy = 0
    ex = 0
    ey = 0
    for child in children:
        pos = child.GetPosition()
        # XXX both margin and padding?
        w = child._get_width() + child.margin_left + child.margin_right + \
            child.padding_left + child.padding_right
        h = child._get_height() + child.margin_top + child.margin_bottom + \
            child.padding_top + child.padding_bottom

        sx = min(sx, pos[0])
        ex = max(ex, pos[0] + w)

        sy = min(sy, pos[1])
        ey = max(ey, pos[1] + h)

    return (sx, sy, ex - sx, ey - sy)


class RoundedRectangle(Component):

    def __init__(self, parent, x, y, w, h, radius,
                 ic, oc, ot):
        Component.__init__(self, parent)
        self.SetPosition(x, y)
        self._recreate(w, h, radius, ic, oc, ot)

    def set_size (self, w, h):
        self._width  = w
        self._height = h
        self._need_to_recalculate = True
        
    def _recreate(self, w, h, radius, ic, oc, ot):
        points = 10
        self._width = w
        self._height = h
        self.radius = radius
        self.ic = ic
        self.oc = oc
        self.ot = ot
        x = 0
        y = 0
        s = sf.Shape()
        s.SetOutlineWidth(ot)
        tx = 0
        ty = 0
        radius = float(radius)
        for i in range(points):
            tx += radius / points
            ty = math.sqrt(radius*radius - tx * tx)
            s.AddPoint(tx + x + w - radius, y - ty + radius, ic, oc)

        ty = 0
        for i in range(points):
            ty += radius / points
            tx = math.sqrt(radius * radius - ty * ty)
            s.AddPoint(tx + x + w - radius, y + h - radius + ty, ic, oc)

        tx = 0
        for i in range(points):
            tx += radius / points
            ty = math.sqrt(radius * radius - tx * tx)
            s.AddPoint(x + radius - tx, y + h - radius + ty, ic, oc)

        ty = 0
        for i in range(points):
            ty += radius / points
            tx = math.sqrt(radius * radius - ty * ty)
            s.AddPoint(x - tx + radius, y + radius - ty, ic, oc)
        self._sprite = s

    def _do_recalculate(self, window):
        if self._expand_as_necessary_x \
                or self._expand_as_necessary_y:
            bb = get_bounding_box_for_children(self.children)
            
            w = self._width
            h = self._height
            
            # BUG paddings ?
            if self._expand_as_necessary_x:
                w = bb[2]
                w += self.margin_left + self.margin_right
            if self._expand_as_necessary_y:
                h = bb[3]
                h += self.margin_top + self.margin_bottom

            # XXX back_children ignored
            self._recreate(w, h,
                           self.radius,
                           self.ic,
                           self.oc,
                           self.ot)
        Component._do_recalculate(self, window)

    def _get_unscaled_width(self):
        return self._width

    def _get_unscaled_height(self):
        return self._height
