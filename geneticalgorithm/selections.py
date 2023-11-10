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


class WithElitism(Selection):
    def __init__(self, selection: Selection, random: Random,
                 n_elites: int = 3):
        self.selection = selection
        self.random = random
        self.n_elites = n_elites

    def __call__(self, population: list[str], fitness: Fitness) -> list[str]:
        elites = sorted(population, key=fitness, reverse=True)[:self.n_elites]
        newpop = self.selection(population, fitness)

        to_replace = self.random.sample(range(len(newpop)), k=self.n_elites)
        for i, elite in zip(to_replace, elites):
            newpop[i] = elite

        return newpop
