import dataclasses


@dataclasses
class Newdata(object):

    def __init__(self):
        pass

    def __str__(self):
        pass

    @property
    def context(self) -> str:
        return self._context

    @context.setter
    def context(self, context): self._context = context

    @property
    def fname(self) -> str:
        return self.fname

    @fname.setter
    def fname(self, fname): self.fname = fname


