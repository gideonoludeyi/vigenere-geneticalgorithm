import abc
from random import Random


class Crossover(abc.ABC):
    """base class for crossover operations"""

    @abc.abstractmethod
    def __call__(self, p1: str, p2: str) -> tuple[str, str]:
        pass


class UniformCrossover(Crossover):
    """implementation of uniform crossover (ux)"""

    def __init__(self, random: Random):
        self.random = random

    def __call__(self, p1: str, p2: str) -> tuple[str, str]:
        mask = self.random.getrandbits(len(p1))  # generate random mask
        c1 = list(p1)  # copy parent 1 to child 1
        c2 = list(p2)  # copy parent 2 to child 2
        for i in range(len(p1)):
            if mask & (2**i) == 0:  # mask position is 1
                # copy i-th gene of parent 1 and parent 2
                # onto child 2 and child 1 respectively
                c1[i] = p2[i]
                c2[i] = p1[i]
        return ("".join(c1), "".join(c2))


class OrderCrossover(Crossover):
    """implementation of order crossover (ox)"""

    def __init__(self, random: Random):
        self.random = random

    def __call__(self, p1: str, p2: str) -> tuple[str, str]:
        # compute endpoints
        i, j = self.random.sample(range(len(p1)), k=2)
        i, j = min(i, j), max(i, j)

        # copy parent 1 and parent 2 to child 2 and child 1 respectively
        c1 = list(p2)
        c2 = list(p1)

        # swap genes between start and end points
        c1[i:j] = p1[i:j]
        c2[i:j] = p2[i:j]
        return ("".join(c1), "".join(c2))
