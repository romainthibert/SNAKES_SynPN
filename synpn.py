from snakes import ConstraintError
import snakes.plugins

@snakes.plugins.plugin("snakes.nets")
def extend(module):

    class PetriNet(module.PetriNet):
        def __init__(self, name, E={}):
            self.E = E
            self.activeEvent = None
            module.PetriNet.__init__(self,name)

        def simulation(self):
            print("Simulation start. Current activeEvent is {}".format(self.activeEvent))
            run=True
            while run:
                stable=False
                while not stable:
                    stable=True
                    for t in self.transition():
                        bind=t.modes()
                        if t.enabled(bind):
                            t.fire(bind)
                            print(t,"fired")
                            stable=False

                nextEvent=input("Stable marking reached.\n====\nNext event ? (q to exit)\n")

                if nextEvent == 'q':
                    break

                self.activeEvent=nextEvent
                for t in self.transition():
                    bind=t.modes()
                    if t.enabled(bind):
                        t.fire(bind)
                        print(t,"fired")
                self.activeEvent=None
                print("Event reset\n====")


    class Transition(module.Transition):
        def __init__(self, name, PN, guard=None, **args):
            self.inputLabel = args.pop("inputLabel",None)
            self.PN = PN
            module.Transition.__init__(self, name, guard=None)

        def enabled(self, binding):
            if self.inputLabel == self.PN.activeEvent:
                return module.Transition.enabled(self, binding)
            elif self.inputLabel == None and self.PN.activeEvent == None:
                return module.Transition.enabled(self, binding)
            else:
                return False


    return Transition, PetriNet
