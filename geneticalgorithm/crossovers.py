import abc
from random import Random


class Crossover(abc.ABC):
    @abc.abstractmethod
    def __call__(self, p1: str, p2: str) -> tuple[str, str]:
        pass


class UniformCrossover(Crossover):
    def __init__(self, random: Random):
        self.random = random

    def __call__(self, p1: str, p2: str) -> tuple[str, str]:
        mask = self.random.getrandbits(len(p1))
        c1 = []
        c2 = []
        for i in range(len(p1)):
            if mask & (2**i) != 0:
                c1.append(p1[i])
                c2.append(p2[i])
            else:
                c1.append(p2[i])
                c2.append(p1[i])
        return ("".join(c1), "".join(c2))


class OrderCrossover(Crossover):
    def __init__(self, random: Random):
        self.random = random

    def __call__(self, p1: str, p2: str) -> tuple[str, str]:
        i, j = self.random.sample(range(len(p1)), k=2)
        i, j = min(i, j), max(i, j)
        c1 = list(p2)
        c2 = list(p1)

        c1[i:j] = p1[i:j]
        c2[i:j] = p2[i:j]
        return ("".join(c1), "".join(c2))
