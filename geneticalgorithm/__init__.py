from collections.abc import Generator
from string import ascii_lowercase
from random import Random
from dataclasses import dataclass

from .mutations import Mutation
from .crossovers import Crossover
from .selections import Selection
from .evaluators import Evaluator


ALLELES = tuple(ascii_lowercase + "-")  # a-z and special "-" character


@dataclass
class Parameters:
    chromosome_length: int
    initial_population_size: int
    max_generation_span: int
    crossover_rate: float
    mutation_rate: float


def genetic_algorithm(
    params: Parameters,
    crossover: Crossover,
    *,
    mutation: Mutation,
    selection: Selection,
    fitness: Evaluator,
    rng: Random,
) -> Generator[dict[str, float], None, None]:
    """implementation of the genetic algorithm
    it takes the parameters as input, along with implementations
    for the crossover, mutation, selection, and evaluation algorithms.

    The result is an iterator that yields the list of fitness values for each generation,
    allowing the calling the code to access the fitness values during each generation.
    """
    pop = initpopulation(
        params.initial_population_size, params.chromosome_length, random=rng
    )

    for gen in range(1, params.max_generation_span + 1):
        # evaluate fitnesses
        fitnesses = {c: fitness(c) for c in pop}

        # selection
        pop = selection(pop, fitness=lambda c: -fitnesses[c])

        # crossover
        for i in range(0, len(pop), 2):
            if rng.random() < params.crossover_rate:
                pop[i], pop[i + 1] = crossover(pop[i], pop[i + 1])

        # mutation
        for i in range(len(pop)):
            if rng.random() < params.mutation_rate:
                pop[i] = mutation(pop[i])

        yield fitnesses


def initpopulation(
    pop_size: int, chromosome_length: int, *, random: Random
) -> list[str]:
    """generates the initial population set for the genetic algorithm"""
    return [
        "".join(random.choices(ALLELES, k=chromosome_length)) for _ in range(pop_size)
    ]
