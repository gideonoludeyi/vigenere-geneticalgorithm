from collections.abc import Generator
from string import ascii_lowercase
from random import Random
from dataclasses import dataclass

from .mutations import Mutation
from .crossovers import Crossover
from .selections import Selection
from .evaluators import Evaluator


ALLELES = tuple(ascii_lowercase + "-")

DEFAULT_RNG = Random()


@dataclass
class Parameters:
    chromosome_length: int
    initial_population_size: int
    max_generation_span: int
    crossover_rate: float
    mutation_rate: float


def genetic_algorithm(params: Parameters, crossover: Crossover, *,
                      mutation: Mutation,
                      selection: Selection,
                      fitness: Evaluator,
                      rng: Random = DEFAULT_RNG,
                      verbose: bool = False,
                      ) -> Generator[dict[str, float], None, tuple[str, float]]:

    pop = initpopulation(params.initial_population_size,
                         params.chromosome_length,
                         random=rng)

    fitnesses = {c: fitness(c) for c in pop}
    for gen in range(1, params.max_generation_span+1):
        yield fitnesses

        # selection
        pop = selection(pop, fitness=lambda c: -fitnesses[c])

        # crossover
        for i in range(0, len(pop), 2):
            if rng.random() < params.crossover_rate:
                pop[i], pop[i+1] = crossover(pop[i], pop[i+1])

        # mutation
        for i in range(len(pop)):
            if rng.random() < params.mutation_rate:
                pop[i] = mutation(pop[i])

        fitnesses = {c: fitness(c) for c in pop}

    solution = max(pop, key=lambda chromosome: -fitnesses[chromosome])
    return solution, fitnesses[solution]


def initpopulation(pop_size: int, chromosome_length: int, *,
                   random: Random) -> list[str]:
    return ["".join(random.choices(ALLELES, k=chromosome_length))
            for _ in range(pop_size)]
