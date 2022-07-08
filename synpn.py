from snakes import ConstraintError
import snakes.plugins

@snakes.plugins.plugin("snakes.nets")
def extend(module):

    class PetriNet(module.PetriNet):
        def __init__(self, name, E={}):
            self.E = E
            self.activeEvent = None
            module.PetriNet.__init__(self,name)

    class Transition(module.Transition):
        def __init__(self, name, PN, guard=None, **args):
            self.inputLabel = args.pop("inputLabel",None)
            self.PN = PN
            module.Transition.__init__(self, name, guard=None)

        def enabled(self, binding):
            if self.inputLabel == self.PN.activeEvent:
                return module.Transition.enabled(self, binding)
            elif self.inputLabel == None:
                return module.Transition.enabled(self, binding)
            else:
                return False


    return Transition, PetriNet
