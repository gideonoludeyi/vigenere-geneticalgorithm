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
                      ) -> Generator[dict[str, float], None, None]:
    pop = initpopulation(params.initial_population_size,
                         params.chromosome_length,
                         random=rng)

    for gen in range(1, params.max_generation_span+1):
        fitnesses = {c: fitness(c) for c in pop}

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

        yield fitnesses


def initpopulation(pop_size: int, chromosome_length: int, *,
                   random: Random) -> list[str]:
    return ["".join(random.choices(ALLELES, k=chromosome_length))
            for _ in range(pop_size)]


def initpop(pop_size: int, chromosome_length: int, *,
            random: Random) -> list[str]:
    expected_frequencies = [
        0.085,
        0.016,
        0.0316,
        0.0387,
        0.121,
        0.0218,
        0.0209,
        0.0496,
        0.0733,
        0.0022,
        0.0081,
        0.0421,
        0.0253,
        0.0717,
        0.0747,
        0.0207,
        0.001,
        0.0633,
        0.0673,
        0.0894,
        0.0268,
        0.0106,
        0.0183,
        0.0019,
        0.0172,
        0.0011,
    ]
    nullchar_freq = 0.15  # frequency of "-" char

    weights = [x/(1 + nullchar_freq)
               for x in expected_frequencies + [nullchar_freq]]
    return ["".join(random.choices(ALLELES, weights=weights, k=chromosome_length))
            for _ in range(pop_size)]
