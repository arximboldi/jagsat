#
#  Copyright (C) 2009 TribleFlame Oy
#  
#  This file is part of TF.
#  
#  TF is free software: you can redistribute it and/or
#  modify it under the terms of the GNU General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#  
#  TF is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
Actions perform manipulation on a graphical primitive over the course of
time. There are actions for e.g. moving and scaling an object.
"""

import sys
import math
from PySFML import sf
from tf.gfx.imagefile import ImageFile
import tf.behavior.gameloop
import random

from tf.gfx import uihelp

__all__ = [
'Action',
'InstantaneousAction',
'TimedAction',
'SpeedAction',
'MoveRelT',
'ScaleS',
'Gradienter',
'PositionRel',
'RotateT',
'RotateS',
'SetPositionRelativeToRotation',
'RotateSteps',
'Wait',
'Fade',
'FlipX',
'FlipY',
'SendEvent',
'Call0',
'Call',
'CallInfinitely0',
'CallInfinitely',
'RemoveObject',
'RemoveMyself',
'MoveViaPoints',
'Hide',
'Show',
'Animate']


class Action(object):
    """An action acts on a specific ui.uicomponent, by e.g. moving or
    rotating it. It is the primary means to make objects change graphically.

    An action is either a subclass of instantaneousaction, timedaction or
    speedaction.

    An InstantaneousAction should complete immediately.

    A TimedAction should complete after the duration has passed. Note
    that by chaining timedactions, you also make sure that the final
    end time for the last action is the sum all the durations of all
    the previous actions in the chain. A timedaction works with wall-clock
    time, regardless of the framerate. Implementation note: TimedActions can
    often be done as wrapper functions to SpeedActions.

    A SpeedAction has no set end time. It provides the get_current_position
    method, which modifies the object according to wall-clock time, regardless
    of the framerate.

    If you only subclass the action class, you will be susceptible to
    different frame rates. Don't do that.
    """

    def __init__(self):
        self.component = None
        # This is set to some other action if we are waiting for it to
        # complete
        self.waiting_for = None
        self.start_time = None
        self.end_time = None

    def _set_component(self, component):
        assert self.component is None
        self.component = component

    def _set_waiting_for(self, act):
        self.waiting_for = act

    def _begin(self):
        """Called when the action starts. It will have a .component."""
        gl = tf.behavior.gameloop.get_game_loop()
        self.start_time = gl.now()

    def _end(self):
        """Called when the action finishes."""
        if self.end_time is None:
            gl = tf.behavior.gameloop.get_game_loop()
            self.end_time = gl.now()

    def step_action(self):
        """
        Main method that will be called as often as possible.  Get the
        level of completeness by calling
        self.get_percentage_complete(), which will range from 0.0 to
        1.0. Your action should do its work to the same level of
        completeness, returning False until it receives
        @percentage_complete at 1.0, and then return True.
        """
        assert 0

    def remove_action(self):
        gl = tf.behavior.gameloop.get_game_loop()
        gl._actionmanager.remove_action(self)


class InstantaneousAction(Action):
    """This action completeles immediately, after its first step_action."""

    def __init__(self):
        Action.__init__(self)


class TimedAction(Action):

    def __init__(self, duration):
        assert isinstance(duration, float) or isinstance(duration, int)
        self.duration = duration
        self.end_time = None
        Action.__init__(self)

    def _begin(self):
        """Called when the action starts. It will have a .component."""
        Action._begin(self)
        if self.waiting_for is not None:
            self.end_time = self.waiting_for.end_time + self.duration
        else:
            self.end_time = self.start_time + self.duration

    def get_percentage_complete(self):
        gl = tf.behavior.gameloop.get_game_loop()
        # Always recalculate the completeness,
        # and make sure it is always [ 0.0, 1.0 ]
        percentage_complete = \
            (gl.now() - self.start_time) \
            / (self.end_time - self.start_time)
        percentage_complete = min(max(percentage_complete, 0.0), 1.0)
        return percentage_complete

    def should_finish(self):
        """
        Returns true if the action should finish, according to the given
        duration.
        """
        gl = tf.behavior.gameloop.get_game_loop()
        return self.end_time <= gl.now()


class SpeedAction(Action):

    def __init__(self, speed):
        """
        Speed is any measurement per second. For example, degrees per
        second, pixels per second etc. Speed can be negative.
        """
        Action.__init__(self)
        self.speed = speed

    def get_current_time(self):
        gl = tf.behavior.gameloop.get_game_loop()
        dt = gl.now() - self.start_time
        return dt

    def get_current_position(self):
        dt = self.get_current_time()
        return dt * self.speed

#class move(action):
#    def __init__(self, nx, ny, speed):
#        action.__init__(self)
#        assert 0


class MoveRelT(TimedAction):

    def __init__(self, dur, dx, dy):
        TimedAction.__init__(self, dur)
        self.relx = dx
        self.rely = dy
        self.mx = 0
        self.my = 0

    def step_action(self):
        if self.should_finish():
            self.component.set_position_delta(self.relx - self.mx,
                                              self.rely - self.my)
            return True
        pc = self.get_percentage_complete()
        dx = self.relx * pc
        dy = self.rely * pc
        mx = dx - self.mx
        my = dy - self.my
        self.mx = dx
        self.my = dy
        self.component.set_position_delta(mx, my)


def MoveRelS(speed, dx, dy):
    """This class-like function returns a new MoveRelT object."""
    dd = uihelp.dist(dx, dy)
    return MoveRelT(dd / speed, dx, dy)


class ScaleS(SpeedAction):

    def __init__(self, speed, scalestart, scaleend):
        SpeedAction.__init__(self, abs(speed))
        self.scalestart = scalestart
        self.scaleend = scaleend

    def _begin(self):
        SpeedAction._begin(self)
        if self.scalestart is None:
            self.scalestart = self.component.GetScale()[0]
        if self.scaleend < self.scalestart:
            self.speed = -self.speed

    def step_action(self):
        scale = self.get_current_position() + self.scalestart
        if self.speed > 0 and scale >= self.scaleend:
            self.component.SetScale(self.scaleend, self.scaleend)
            return True
        elif self.speed < 0 and scale <= self.scaleend:
            self.component.SetScale(self.scaleend, self.scaleend)
            return True
        self.component.SetScale(scale, scale)


class Gradienter(Action):
    """
    Generic class which slides the list values
    from @start to @stop with the speed given in @speed.
    The speed values should be positive.
    """

    def __init__(self, start, speed, stop):
        Action.__init__(self)
        self.start = start
        self.cur = None
        self.stop = stop
        self.speed = list(speed)

    def _gradient_calculate_start(self):
        pass

    def _set_component(self, component):
        Action._set_component(self, component)

        if self.start is None:
            self.start = tuple(self._gradient_calculate_start())

        self.cur = list(self.start)

        for i in range(len(self.cur)):
            if self.speed[i] >= 0 and self.stop[i] < self.start[i]:
                #print self.start, self.speed, self.stop
                self.speed[i] = -self.speed[i]
            elif self.speed[i] <= 0 and self.stop[i] > self.start[i]:
                #print self.start, self.speed, self.stop
                print self.start, self.speed, self.stop
                self.speed[i] = -self.speed[i]

    def step_action(self):
        brk = 0
        for i in range(len(self.cur)):
            self.cur[i] += self.speed[i]
            if self.speed[i] <= 0 and self.cur[i] < self.stop[i]:
                self.cur[i] = self.stop[i]
            elif self.speed[i] >= 0 and self.cur[i] > self.stop[i]:
                self.cur[i] = self.stop[i]

            if self.cur[i] == self.stop[i]:
                brk += 1

        self._gradienter_do()

        if brk == len(self.cur):
            return True

    def _gradienter_do(self):
        # Just override this method.
        assert 0


class PositionRel(Gradienter):
    """Sets the relative position."""

    def __init__(self, pos_start, speed, pos_end):
        Gradienter.__init__(self, pos_start, speed, pos_end)

    def _gradient_calculate_start(self):
        p = self.component.GetPosition()
        w = self.component.get_window()
        px = p[0] / w.window.GetWidth()
        py = p[1] / w.window.GetHeight()
        return px, py

    def _gradienter_do(self):
        self.component.set_position_rel(self.cur[0],
                                        self.cur[1])


def rotate_distance(startrot, endrot):
    startrot = uihelp.clamp_angle(startrot)
    endrot = uihelp.clamp_angle(endrot)
    s = endrot - startrot
    dir = 1
    if s < 0:
        s += 360
    if s > 180:
        s = 360 - s
        dir = -1
    if s < 0 or s > 180:
        print "tf: rotate_distance: Internal error", startrot, endrot, s
        assert 0

    assert s >= 0
    assert s <= 180
    return s, dir


class RotateT(TimedAction):
    """
    Rotates a component from @rotatestart to @rotateend, via steps of
    @deltarotate. Measured in degrees.

    If @fastest is true, the component will rotate either clockwise or
    counterclockwise, whichever will lead fastest to the desired result.

    If @rotateend is None, the rotation will never stop. In this case,
    @fastest is ignored.
    """

    def __init__(self, dur, rotatestart, rotateend,
                 fastest = True):
        TimedAction.__init__(self, dur)
        self.rotatestart = uihelp.clamp_angle(rotatestart)
        self.rotateend = uihelp.clamp_angle(rotateend)
        self.dir = 1
        self.distance = self.rotateend - self.rotatestart
        if self.distance < 0:
            self.distance += 360
        if fastest:
            self.distance, self.dir = \
                rotate_distance(self.rotatestart, self.rotateend)

    def step_action(self):
        if self.should_finish():
            self.component.SetRotation(self.rotateend)
            return True
        c = self.component
        pc = self.get_percentage_complete()
        r = self.distance * self.dir * pc + self.rotatestart
        self.component.SetRotation(r)


class RotateS(SpeedAction):
    """
    Rotates a component from @rotatestart to @rotateend, with the
    speed in @speed, measured in degrees / speed.

    If @fastest is true, the component will rotate either clockwise or
    counterclockwise, whichever will lead fastest to the desired result.

    If @rotateend is None, the rotation will never stop. In this case,
    @fastest is ignored.
    """

    def __init__(self, speed, rotatestart, rotateend,
                 fastest = True):
        SpeedAction.__init__(self, speed)
        self.rotatestart = uihelp.clamp_angle(rotatestart)
        if rotateend is None:
            self.rotateend = None
        else:
            self.rotateend = uihelp.clamp_angle(rotateend)

        self.dir = 1
        if self.rotateend:
            self.distance = self.rotateend - self.rotatestart
            if self.distance < 0:
                self.distance += 360
        else:
            self.distance = 0

        if fastest and self.rotateend:
            self.distance, self.dir = \
                rotate_distance(self.rotatestart, self.rotateend)

    def step_action(self):
        c = self.component
        d = self.get_current_position()
        if self.rotateend and d >= self.distance:
            self.component.SetRotation(self.rotateend)
            return True

        r = self.rotatestart + d * self.dir
        self.component.SetRotation(r)


class SetPositionRelativeToRotation(Action):
    """
    This action rotates the object around the screen until
    it has stopped rotating. In other words, you must have an appropriate
    action that rotates the object parallell to this action.
    """

    def __init__(self, relx, rely):
        Action.__init__(self)
        self.relx = relx
        # Some weirdness in the actual calculation,
        # so that's why 1 - rely instead of only rely
        self.rely = 1 - rely
        self.oldrot = None

    def step_action(self):
        r = self.component.GetRotation()

        if r == self.oldrot:
            return True
        self.oldrot = r

        r = -r + 180

        dx = self.relx - 0.5
        dy = self.rely - 0.5
        r = math.radians(r)
        s = math.sin(r)
        c = math.cos(r)
        relx = 0.5 + dx * c - dy * s
        rely = 0.5 + dx * s + dy * c
        self.component.set_position_rel(relx, rely)
        return False


class RotateSteps(Action):

    def __init__(self, deltarotate, steps):
        assert 0
        Action.__init__(self)
        self.deltarotate = deltarotate
        self.steps = steps

    def step_action(self):
        c = self.component
        r = c.GetRotation()
        r += self.deltarotate
        self.component.SetRotation(r)

        self.steps -= 1
        if self.steps == 0:
            return True
        return False


class Wait(TimedAction):

    def __init__(self, dur):
        TimedAction.__init__(self, dur)

    def step_action(self):
        if self.should_finish():
            return True
        return False


class Fade(Action):
    """Fades the component to a fraction of full brightness."""

    def __init__(self, color_start, speed, color_end):
        """color = (255, 255, 255, 255) means full, 0 means black """
        Action.__init__(self)
        self.color_start = color_start
        self.color_end = color_end
        self.speed = list(speed)

    def _begin(self):
        Action._begin(self)
        if self.color_start is None:
            c = self.component.GetColor()
            self.color_start = int(c.r), int(c.g), int(c.b), int(c.a)
        self.color_now = list(self.color_start)
        for i in range(len(self.color_now)):
            if self.speed[i] >= 0 and \
                    self.color_end[i] < self.color_start[i]:
                print self.color_start, self.speed, self.color_end
                self.speed[i] = -self.speed[i]
                #assert 0
            elif self.speed[i] <= 0 and \
                    self.color_end[i] > self.color_start[i]:
                print self.color_start, self.speed, self.color_end
                self.speed[i] = -self.speed[i]
                #assert 0

    def step_action(self):
        brk = 0
        for i in range(len(self.color_now)):
            self.color_now[i] += self.speed[i]
            if self.speed[i] <= 0 and self.color_now[i] < self.color_end[i]:
                self.color_now[i] = self.color_end[i]
            elif self.speed[i] >= 0 and self.color_now[i] > self.color_end[i]:
                self.color_now[i] = self.color_end[i]

            if self.color_now[i] == self.color_end[i]:
                brk += 1
        c = sf.Color(self.color_now[0],
                     self.color_now[1],
                     self.color_now[2],
                     self.color_now[3])
        if hasattr(self.component, "_sprite"):
            if hasattr(self.component._sprite, "GetNbPoints"):
                for i in range(self.component._sprite.GetNbPoints()):
                    self.component._sprite.SetPointColor(i, c)
            self.component._sprite.SetColor(c)
        self.component.set_color(c)

        if brk == 4:
            return True


def FadeOut(speed = 10):
    return Fade((255, 255, 255, 255),
                (0, 0, 0, -speed),
                (255, 255, 255, 0))


def FadeIn(speed = 10):
    return Fade((255, 255, 255, 0),
                (0, 0, 0, speed),
                (255, 255, 255, 255))


class FlipX(InstantaneousAction):

    def __init__(self, flip):
        InstantaneousAction.__init__(self)
        self.flip = flip

    def step_action(self):
        self.component._sprite.FlipX(self.flip)
        return True


class FlipY(InstantaneousAction):

    def __init__(self, flip):
        InstantaneousAction.__init__(self)
        self.flip = flip

    def step_action(self):
        self.component._sprite.FlipY(self.flip)
        return True


class SendEvent(InstantaneousAction):
    """
    Sends an @Event on a @Signal.
    """

    def __init__(self, signal, event):
        InstantaneousAction.__init__(self)
        self.signal = signal
        self.event = event

    def step_action(self):
        self.signal.call(self.event)
        return True


class Call0(InstantaneousAction):
    """
    Calls a given function with given arguments and keyword arguments.
    """

    def __init__(self, func, *args, **kwargs):
        InstantaneousAction.__init__(self)
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def step_action(self):
        self.func(*self.args, **self.kwargs)
        return True


class Call(InstantaneousAction):
    """
    Calls a given function with given arguments and keyword arguments.
    The first argument given is the component that this action was bound.
    """

    def __init__(self, func, *args, **kwargs):
        InstantaneousAction.__init__(self)
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def step_action(self):
        self.func(self.component, *self.args, **self.kwargs)
        return True


class CallInfinitely0(InstantaneousAction):
    """
    Calls a function every tick.

    NOTE: This will use up CPU whether or not you actually do
    something in your action. So please use something else.
    """

    def __init__(self, func, *args, **kwargs):
        InstantaneousAction.__init__(self)
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def step_action(self):
        return self.func(*self.args, **self.kwargs)


class CallInfinitely(InstantaneousAction):
    """
    Calls a function every tick, with the first argument being the
    component that this action was bound.

    NOTE: This will use up CPU whether or not you actually do
    something in your action. So please use something else.
    """


    def __init__(self, func, *args, **kwargs):
        InstantaneousAction.__init__(self)
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def step_action(self):
        return self.func(self.component, *self.args, **self.kwargs)


class RemoveObject(InstantaneousAction):
    """
    Removes an object from the user interface. The object should not
    be used afterwards.
    """

    def __init__(self, obj):
        InstantaneousAction.__init__(self)
        self.obj = obj

    def step_action(self):
        self.obj.remove_myself()
        return True


class RemoveMyself(InstantaneousAction):
    """
    Removes the object bound to this action from the user
    interface. The object should not be used afterwards.
    """

    def __init__(self):
        InstantaneousAction.__init__(self)

    def step_action(self):
        self.component.remove_myself()
        return True


class MoveViaPoints(Action):
    """ BUG untested"""

    def __init__(self, points, timesteps):
        assert 0
        self.points = points
        self.timesteps = timesteps
        self.idx = 0
        self._calculate()

    def _calculate(self):
        assert len(self.points) >= 2
        dist = 0
        self.dist_by_point = []
        basex = self.points[0][0]
        basey = self.points[0][1]
        self.deltas = []
        for i, p in enumerate(self.points):
            dx = p[0] - basex
            dy = p[1] - basey
            d = uihelp.dist(dx, dy)
            dist += d
            self.dist_by_point.append(dist)
            self.deltas.append((dx, dy))
            basex = p[0]
            basey = p[1]

        self.dist = dist
        self.dist_by_step = self.dist / float(self.timesteps)
        self.curdist = 0
        self.prev_dx = 0
        self.prev_dy = 0

    def step_action(self):
        self.curdist += self.dist_by_step
        if self.curdist >= self.dist_by_point[self.idx + 1]:
            self.idx += 1
            if self.idx >= len(self.dist_by_point):
                #self.component.set_position_move_delta(dx, dy)
                return True
        extradist = self.curdist - self.dist_by_point[self.idx]
        dd = self.dist_by_point[self.idx+1] - self.dist_by_point[self.idx]
        frac = extradist / float(dd)
        delta = self.deltas[self.idx + 1]
        dx = delta[0] * frac
        dy = delta[1] * frac
        rdx = dx - self.prev_dx
        rdy = dy - self.prev_dy
        self.prev_dx = dx
        self.prev_dy = dy
        self.component.set_position_move_delta(rdx, rdy)


class Hide(InstantaneousAction):
    """
    Hides a component. Any children are also hidden.
    """

    def __init__(self):
        InstantaneousAction.__init__(self)

    def step_action(self):
        self.component.set_visible(False)
        return True


class Show(InstantaneousAction):
    """
    Shows the component (assuming that all parents are also shown.
    """

    def __init__(self):
        InstantaneousAction.__init__(self)

    def step_action(self):
        self.component.set_visible(True)
        return True


def ShowOrHide(show_p):
    """
    Show or hide a component based on @show_p.
    """
    if show_p:
        return Show()
    else:
        return Hide()


def move_out(component, speed):
    win = component.get_window()
    speed = 1200
    w = win.window.GetWidth()
    h = win.window.GetHeight()
    x = random.randrange(0, 4)
    dx, dy = [(w, 0), (-w, 0), (0, h), (0, -h)][x]
    component.add_action_sequence(
        [MoveRelS(speed, dx, dy),
         Hide()])


def move_in(component, speed):
    win = component.get_window()
    speed = 1200
    # BUG parent chain?
    if component.parent:
        w = component.parent._get_width()
        h = component.parent._get_height()
    else:
        w = win.window.GetWidth()
        h = win.window.GetHeight()

    x = random.randrange(0, 4)

    destx = w / 2.0
    desty = h / 2.0

    dx, dy = [(w, 0), (-w, 0), (0, h), (0, -h)][x]

    component.SetPosition(-dx + destx, -dy + desty)
    component.add_action_sequence([Show(),
                                   MoveRelS(speed, dx, dy)])


class Animate(Action):
    """
    Animate a tf.gfx.Image forever.
    """

    def __init__(self, filenames, anim_speed):
        Action.__init__(self)
        self.anim_speed = anim_speed
        self.tick_count = self.anim_speed
        self.images = []
        self.cur = -1
        if isinstance(filenames, str):
            i = 1
            while True:
                try:
                    img = ImageFile.new_image(filenames % i)
                    print "IMG", filenames, i
                except:
                    print sys.exc_value
                    break
                self.images.append(img)
                i += 1
        else:
            for f in filenames:
                img = imagefile.new_image(f)
                self.images.append(img)

        assert len(self.images) > 0

    def step_action(self):
        self.tick_count += 1
        if self.tick_count >= self.anim_speed:
            self.tick_count = 0
        else:
            return
        img = self.images[self.cur]
        self.component.set_image(img)
        self.cur += 1
        if self.cur >= len(self.images):
            self.cur = 0
