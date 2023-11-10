import abc
from random import Random


class Mutation(abc.ABC):
    @abc.abstractmethod
    def __call__(self, c: str) -> str:
        pass


class ReciprocalExchangeMutation(Mutation):
    def __init__(self, random: Random):
        self.random = random

    def __call__(self, chromosome: str) -> str:
        i, j = self.random.sample(range(len(chromosome)), k=2)
        chars = list(chromosome)
        chars[i], chars[j] = chars[j], chars[i]
        return "".join(chars)


class RandomCharacterMutation(Mutation):
    def __init__(self, alleles: list[str], random: Random):
        self.random = random
        self.alleles = alleles

    def __call__(self, chromosome: str) -> str:
        i = self.random.choice(range(len(chromosome)))
        chars = list(chromosome)
        chars[i] = self.random.choice(self.alleles)
        return "".join(chars)
