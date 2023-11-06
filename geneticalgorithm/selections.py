import abc
from typing import Callable
from random import Random


Fitness = Callable[[str], float]


class Selection(abc.ABC):
    @abc.abstractmethod
    def __call__(self, population: list[str], fitness: Fitness) -> list[str]:
        pass


class TournamentSelection(Selection):
    def __init__(self, k: int, random: Random):
        self.k = k
        self.random = random

    def __call__(self, population: list[str], fitness: Fitness) -> list[str]:
        selections = []
        for i in range(len(population)):
            chromosomes = self.random.sample(population, k=self.k)
            selected = max(chromosomes, key=fitness)
            selections.append(selected)
        return selections
