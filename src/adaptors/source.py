import typing

class Result:
    def __str__(self) -> str:
        raise NotImplemented()

class Source:
    def all(self) -> typing.Sequence[Result]:
        raise NotImplemented()

    def next(self) -> Result:
        raise NotImplemented()

    def filter(self, filterFunc: typing.Callable[[Result], bool]) -> typing.Sequence[Result]:
        return filter(filterFunc, self.all())

