import abc
from random import Random


class Mutation(abc.ABC):
    @abc.abstractmethod
    def name(self) -> str:
        pass

    @abc.abstractmethod
    def __call__(self, c: str) -> str:
        pass


class ReciprocalExchangeMutation(Mutation):
    def __init__(self, random: Random):
        self.random = random

    def name(self) -> str:
        return "Reciprocal Exchange"

    def __call__(self, chromosome: str) -> str:
        i, j = self.random.sample(range(len(chromosome)), k=2)
        chars = list(chromosome)
        chars[i], chars[j] = chars[j], chars[i]
        return "".join(chars)
