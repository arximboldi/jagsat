#
# Copyright (C) 2009 The JAGSAT project team.
#
# This software is in development and the distribution terms have not
# been decided yet. Therefore, its distribution outside the JAGSAT
# project team or the Project Course evalautors in Abo Akademy is
# completly forbidden without explicit permission of their authors.
#
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from base.util import *
from weakref import proxy
from error import *
from base.log import *
from base import util
import math
from functools import partial

_log = get_log (__name__)


class TaskError (CoreError):
    pass


killed  = 0
running = 1
paused  = 2

class Task (object):

    def __init__ (self, *a, **k):
        super (Task, self).__init__ (*a, **k)
        self._state = running
        self._next  = []
        self._task_manager = None

    def do_update (self, timer):
        pass

    def do_restart (self):
        pass
    
    def add_next (self, task):
        self._next.append (task)
        return task
    
    def update (self, timer):
        if self._state == running:
            self.do_update (timer)
        return self._state
    
    def pause (self):
        if self._state != killed:
            self._state = paused

    def resume (self):
        if self._state != killed:
            self._state = running

    def toggle_pause (self):
        if self._state != killed:
            self._state = running if self._state == paused else paused
    
    def restart (self):
        self.do_restart ()
        self._state = running

    def kill  (self):
        self._state = killed
        if self._task_manager:
            for task in self._next:
                self._task_manager.add (task)
        
    def is_paused (self):
        return self._state == paused

    def is_killed (self):
        return self._state == killed

    @property
    def state (self):
        return self._state

    @property
    def parent_task (self):
        return self._task_manager
    
    def _set_parent (self, manager):
        if self._task_manager and manager:
            raise TaskError ("Already attached to: " + str (self._task_manager))
        self._task_manager = manager


class WrapperTask (Task):
    
    def __init__ (self, wrapped_task = None, *a, **k):
        super (WrapperTask, self).__init__ (*a, **k)
        self.wrapped_task = wrapped_task

    def update (self, timer):
        super (WrapperTask, self).update (timer)
        self.wrapped_task.update (timer)
        
    def _set_parent (self, manager):
        super (WrapperTask, self)._set_parent (manager)
        self.wrapped_task._set_parent (manager)


class FuncTask (Task):

    def __init__ (self, func = None, *a, **k):
        assert func != None
        super (FuncTask, self).__init__ (*a, **k)
        self._set_func (func)
        
    def _set_func (self, func):
        if func.func_code.co_argcount < 1:
            self._orig = func
            self._func = lambda t: func ()
        else:
            self._orig = self._func = func

    def _get_func (self):
        return self._orig
    
    def do_update (self, timer):
        super (FuncTask, self).do_update (timer)
        action = self._func (timer)
        if not action or action == killed:
            self.kill ()
        elif action == paused:
            self.pause ()

    func = property (_get_func, _set_func)


def totask (task):
    if not isinstance (task, Task):
        if not callable (task):
            raise TaskError ('You can add either tasks or callables. ' +
                             str(task))
        task = FuncTask (func = task)    
    return task


class TaskGroup (Task):

    auto_kill   = True
    auto_remove = True
    loop        = False
    
    def __init__ (self,
                  tasks = [],
                  auto_kill = None,
                  auto_remove = None,
                  loop = None,
                  *a, **k):
        super (TaskGroup, self).__init__ (*a, **k)

        if auto_kill is not None:
            self.auto_kill = auto_kill
        if auto_remove is not None:
            self.auto_remove = auto_remove
        if loop is not None:
            self.loop = loop
        
        self._tasks = []
        for task in tasks:
            self.add (task)

    def __del__ (self):
        self.clear ()
    
    def clear (self):
        for t in self._tasks:
            t._set_parent (None)
        self._tasks = []
        
    def do_update (self, timer):
        super (TaskGroup, self).do_update (timer)
        for task in self._tasks:
            task.update (timer)
        if self.auto_remove:
            self._tasks = remove_if (Task.is_killed, self._tasks)

        all_killed = len (filter (Task.is_killed, self._tasks)) == self.count
        if self.auto_kill and all_killed:               
            self.kill ()
        elif self.loop and all_killed:
            self.restart ()
    
    def add (self, task):
        task = totask (task)
        task._set_parent (self)
        self._tasks.append (task)
        return task

    def remove (self, task):
        self._tasks.remove (task)
        task._set_parent (None)

    def find (self, func):
        for task in self._tasks:
            if isinstance (task, FuncTask) and \
               task.func == func:
                return task

    def restart (self):
        super (TaskGroup, self).restart ()
        for x in self._tasks:
            x.restart ()

    @property
    def count (self):
        return len (self._tasks)


class WaitTask (Task):

    duration = 1.
    
    def __init__ (self, duration = None, *a, **k):
        super (WaitTask, self).__init__ (*a, **k)
        if duration is not None:
            self.duration = duration
        self.remaining = self.duration

    def do_update (self, timer):
        super (WaitTask, self).do_update (timer)
        self.remaining -= timer.delta
        if self.remaining <= 0:
            self.kill ()
            self.remaining = 0

    def do_restart (self):
        self.remaining = self.duration

class DelayTask (Task):

    duration = 1
    
    def __init__ (self, duration = None, *a, **k):
        super (DelayTask, self).__init__ (*a, **k)
        if duration is not None:
            self.duration = duration
        self.remaining = self.duration

    def restart_wait (self):
        self.remaining = self.duration
                
    def do_update (self, timer):
        super (DelayTask, self).do_update (timer)
        self.remaining -= 1
        if self.remaining < 0:
            self.kill ()
            self.remaining = 0
            

class TimerTask (WaitTask):

    def do_update (self, timer):
        super (TimerTask, self).do_update (timer)
        if self.remaining == 0:
            self.on_finish ()
        else:
            self.on_tick ()
    
    def on_tick (self):
        pass

    def on_finish (self):
        pass


class FadeTask (Task):

    def __init__ (self,
                  func = nop,
                  duration = 1.0,
                  loop = False,
                  init = False,
                  *a, **k):
        super (FadeTask, self).__init__ (*a, **k)
        self.func      = func
        self.curr      = 0.
        self.loop      = loop
        self.duration = duration

        if init: 
            func (0.0)

    def do_update (self, timer):
        super (FadeTask, self).do_update (timer)
        self.func (self.curr / self.duration)
        self.curr += timer.delta / self.duration

        if self.curr >= self.duration:
            if self.loop:
                self.curr -= self.duration
            else:
                self.curr = self.duration
                self.kill ()
                self.func (self.curr)


class FuncWaitTask (WaitTask):
    def __init__ (self, wait_func = None, *a, **k):
        super (FuncWaitTask, self).__init__ (duration = wait_func (), *a, **k)
        self.wait_func = wait_func

    def do_restart (self):
        self.duration = self.wait_func ()
        self.remaining = self.duration


def sequence (fst, *tasks):
    task  = totask (fst)
    tasks = map (totask, tasks)

    for nxt in tasks:
        task = task.add_next (nxt)

    return fst

def parallel (*tasks):
    return TaskGroup (tasks = tasks,
                      auto_remove = False)

def loop (*tasks):
    return TaskGroup (tasks = tasks,
                      auto_remove = False,
                      auto_kill = False,
                      loop = True)

func_wait = FuncWaitTask

wait = WaitTask

fade = FadeTask

delay = DelayTask

def invfade (f, *a, **k):
    return fade (lambda x: f (1.0 - x), *a, **k)

def linear (f, min, max, *a, **k):
    return fade (lambda x: f (util.linear (min, max, x)), *a, **k)

def sinusoid (f, min = 0.0, max = 1.0, *a, **k):
    return fade (
        lambda x: f (min + (max - min) * math.sin (x * math.pi / 2.)), *a, **k)

def run (func):
    return FuncTask (lambda t: None if func () else None)

def repeat (task):
    task = totask (task)
    task.kill = task.restart    
    return WrapperTask (task)
