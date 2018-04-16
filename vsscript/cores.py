from vsscript.vs_capi import Script

from yuuno import Yuuno
from yuuno.clip import Clip, Frame
from yuuno.core.environment import Environment


class CoreHost(Environment):
    """
    Implement a core host
    """

    @classmethod
    def start(cls, **kwargs):
        controller = Yuuno.instance()
        env = cls(parent=controller, **kwargs)
        controller.environment = env
        controller.start()
        return env

    def initialize(self):
        pass

    def deinitialize(self):
        pass


class EmbeddedClip(Clip):

    def __init__(self, parent, core):
        self.parent = parent
        self.core = core

    def __len__(self):
        return len(self.parent)

    def __getitem__(self, item):
        def _cb():
            return EmbeddedFrame(self.parent[item], self.core)
        return self.core.run_inside_script(_cb)


class EmbeddedFrame(Frame):
    def __init__(self, parent, core):
        self.parent = parent
        self.core = core

    def to_pil(self):
        def _cb():
            return self.parent.to_pil()
        return self.core.run_inside_script(_cb)


class EmbeddedCore(object):

    def __init__(self):
        self.script = None

    def stop(self):
        if self.script is None:
            return
        self.script.dispose()
        self.script = None

    def start(self):
        if self.script is not None:
            raise RuntimeError("There is already a running core.")
        self.script = Script()

    def restart(self):
        self.stop()
        self.start()

    def push_code(self, code):
        self.restart()
        self.script.exec(code)

    def list_output_ids(self):
        return tuple(self.script.outputs.values())

    def get_output(self, id=0):
        return EmbeddedClip(Yuuno.instance().wrap(self.script.outputs[id]), self)

    def run_inside_script(self, cb):
        return self.script.perform(cb)


class EmbeddedCoreProvider(object):

    def create(self) -> EmbeddedCore:
        return EmbeddedCore()


if __name__ == '__main__':
    env = CoreHost.start()
    cp = EmbeddedCoreProvider()
    embedded_core = cp.create()
    embedded_core.push_code('import vapoursynth as vs; vs.core.std.BlankClip().set_output()')
    print(embedded_core.get_output()[0].to_pil())