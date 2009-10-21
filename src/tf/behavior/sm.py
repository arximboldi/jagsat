#
# This file is copyright Tribeflame Oy, 2009.
#
from tf.gfx import ui

from tf import signalslot


#class StateMachine(object):
#
#    def __init__(self, name, start_state):
#        self.name = name
#        self._start_state = start_state
#
#    def execute(self):
#        return Execution(self, self._start_state)


#class Execution(object):


class StateMachine(object):
    """
    The execution of a statemachine. When forking/joining in
    statemachines, it is important to be able to keep track of what is
    happening.  An Execution object keeps track of the current parent
    chain of states.
    """

    def __init__(self, name, start_state):
        self.name = name
        self._statelist = []
        self._gameloop = None
        self._rootstate = State() # Dummy root state
        self._rootstate._statemachine = self
        self._rootstate._gameloop = None
        self._start_state_for_root = start_state

    def start(self, gameloop):
        print "tf: Starting execution of statemachine", self.name
        #, "(statemachine", self._state._statemachine, ")"
        self._rootstate._gameloop = gameloop
        self._rootstate.enter_substate(self._start_state_for_root)

    def do_statemachine(self, gameloop):
        #print "Executing statemachine", self.name
        ret = self._rootstate.work()
        assert ret is None
        assert self._rootstate._substate is not None

    def get_current_state(self):
        s = self._rootstate
        while s:
            if s._substate is None:
                return s
            s = s._substate
        assert 0


class State(object):

    def __init__(self): #, sm, execution):
        #self._statemachine = sm
        #self._execution = execution
        #self._gameloop
        self._exit_callbacks = set()
        self._signals_and_targets = []

        # Superstate
        self._superstate = None
        # Substate
        self._newsubstate = None
        self._substate = None
        # Variables defined in this statemachine
        self._variables = {}

    def __str__(self):
        str = []
        p = self
        while p:
            str.append(p.__class__.__name__)
            p = p._superstate
        str.reverse()
        return ".".join(str)

    def get_variable(self, var):
        """Returns a statemachine variable, either from this
        state or any parent superstate."""
        s = self
        while s:
            try:
                return s._variables[var]
            except KeyError:
                s = s._superstate
        raise ValueError("Invalid statemachine variable " + var + "!")

    def set_variable(self, var, value):
        """Sets a variable, either in this state or in the
        first parent superstate, depending on who created
        the variable."""
        s = self
        while s:
            try:
                s._variables[var]
            except KeyError:
                s = self._superstate

            s._variables[var] = value
            return

        raise ValueError("Invalid statemachine variable " + var + "!")

    def create_variable(self, var, value):
        """Creates a new variable @var in this state, with the initial
        value @value."""
        assert var not in self._variables
        self._variables[var] = value
        return self._variables[var]

    def _end_all_substates(self, until):
        if self._substate:
            self._substate._end_all_substates(until)
        if self != until:
            self.exit_state()

    def change_state(self, s, *args, **kwargs):
        if self._superstate is None:
            self._statemachine.change_state(s, *args, **kwargs)
            return
        self._end_all_substates(self)
        self._superstate._newsubstate = (s, args, kwargs)

    def enter_substate(self, state, *args, **kwargs):
        print "    substate", self._substate
        print "new substate", self._newsubstate
        assert self._substate is None
        assert self._newsubstate is None
        print "Entering substate", state.__name__
        self._newsubstate = state, args, kwargs

    def get_statemachine(self):
        return self._statemachine

    def get_gameloop(self):
        return self._gameloop

    def register_signals(self, tuple_of_signal_and_targets):
        for signal, target in tuple_of_signal_and_targets:
            signal.add(target)
            self._signals_and_targets.extend(tuple_of_signal_and_targets)

    def register_signal(self, signal, target):
        signal.add(target)
        self._signals_and_targets.extend([(signal, target)])

    def add_exit_callback(self, func):
        self._exit_callbacks.add(func)

    def add_transient_ui(self, a):
        """Add a user interface that will be removed when the state exits."""
        self.add_exit_callback(lambda: a.remove_myself())

    def enter_state(self, *args, **kwargs):
        self.do_enter_state(*args, **kwargs)

    def work(self):
        if self._newsubstate:
            if self._substate is not None:
                print "tf: Statemachine", self._statemachine.name, \
                    "exiting substate", str(self._substate)
                self._substate.exit_state()

            assert self._substate is None
            newsubstate, args, kwargs = self._newsubstate
            self._newsubstate = None

            if newsubstate == StateFinal:
                print "tf: Statemachine", self._statemachine.name, \
                    "ending submachine."
                assert self._substate == None
                assert self._newsubstate == None
                return

            self._substate = newsubstate()
            self._substate._statemachine = self._statemachine
            self._substate._superstate = self
            self._substate._gameloop = self._gameloop
            print "tf: Statemachine", self._statemachine.name, \
                "entering substate", str(self._substate)
            print "tf: - Arguments:", args
            print "tf: - Keyword arguments", kwargs
            ret = self._substate.enter_state(*args, **kwargs)
            assert ret is None
            return

        #print "tf: Working in state", self

        if self._substate:
            self._substate.work()
        else:
            # Only the lowest level does any work.
            self.do_work()

    def exit_state(self):
        self.do_exit_state()
        for f in self._exit_callbacks:
            f()

        for signal, target in self._signals_and_targets:
            signal.remove(target)

        # This will make the superstate continue its work
        if self._superstate:
            if self._superstate._substate != self:
                print "ERROR, I am", self, "but need to be", \
                    self._superstate._substate
            assert self._superstate._substate == self
            self._superstate._substate = None

    def do_enter_state(self, *args, **kwargs):
        """Override this."""
        pass

    def do_work(self):
        """Override this."""
        pass

    def do_exit_state(self):
        """Override this."""
        pass


class StateFinal(State):
    pass
