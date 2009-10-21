#
# This file is copyright Tribeflame Oy, 2009.
#
class ActionManager:

    def __init__(self):
        self.obj2actions = {}
        self.obj2active_actions = {}

    def add_action(self, obj, action, wait_for):
        assert obj is not None
        assert action is not None
        try:
            self.obj2actions[obj]
        except KeyError:
            self.obj2actions[obj] = set()

        self.obj2actions[obj].add(action)

        action._set_component(obj)
        if wait_for:
            self.obj2actions[obj].add(wait_for)
            assert wait_for.component is None or wait_for.component is obj
            action._set_waiting_for(wait_for)
            assert wait_for.component != None
        else:
            action._begin()

            try:
                self.obj2active_actions[obj]
            except KeyError:
                self.obj2active_actions[obj] = []

            self.obj2active_actions[obj].append(action)

    def remove_all_actions(self, obj):
        try:
            del self.obj2actions[obj]
        except KeyError:
            pass

        try:
            del self.obj2active_actions[obj]
        except KeyError:
            pass

    def remove_actions(self, obj, func):
        try:
            actions = self.obj2actions[obj]
        except:
            return

        lst = [i for i in actions if func(i)]
        for act in lst:
            self.remove_action(act)

    def remove_action(self, action):
        # BUG should fix waiting_for!
        self.obj2actions[action.component].remove(action)
        self.obj2active_actions[action.component].remove(action)

    def tick_actions(self, gameloop):
        now = gameloop.now()
        old = dict(self.obj2active_actions)

        empty_list = []

        for obj, active_actions in old.iteritems():
            done = set()

            for action in active_actions:
                assert action.waiting_for is None
                assert action.component
                is_done = action.step_action()
                if is_done:
                    done.add(action)

            for wait_for in done:
                wait_for._end()

                # The key might be missing if some action decided
                # to remove this object
                try:
                    self.obj2active_actions[obj].remove(wait_for)
                except KeyError:
                    pass

                try:
                    self.obj2actions[obj].remove(wait_for)
                except KeyError:
                    pass

            for act in self.obj2actions.get(obj, empty_list):
                if act.waiting_for in done:
                    act._begin()
                    act.waiting_for = None
                    self.obj2active_actions[obj].append(act)

    def get_active_actions(self, obj):
        return self.obj2active_actions[obj]
