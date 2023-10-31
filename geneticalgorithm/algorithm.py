from typing import Callable
from string import ascii_lowercase
from random import Random
from dataclasses import dataclass
# from pprint import pprint

GENES = tuple(ascii_lowercase + "-")


@dataclass
class Parameters:
    chromosome_length: int
    initial_population_size: int
    max_generation_span: int
    crossover_rate: float
    mutation_rate: float
    random_seed: int | None


def genetic_algorithm(text: str, params: Parameters):
    rng = Random(params.random_seed)

    pop = initpopulation(params.initial_population_size,
                         params.chromosome_length,
                         random=rng)

    for gen in range(1, params.max_generation_span+1):
        # selection
        pop = selection(pop,
                        fitness=lambda chromosome: -fitness(chromosome, text),
                        random=rng)

        # crossover
        for i in range(0, len(pop), 2):
            if rng.random() < params.crossover_rate:
                pop[i], pop[i+1] = crossover(pop[i], pop[i+1], random=rng)

        # mutation
        for i in range(len(pop)):
            if rng.random() < params.mutation_rate:
                pop[i] = mutate(pop[i], random=rng)

    # pprint(sorted([(chromosome, fitness(chromosome, text))
    #                for chromosome in pop], key=lambda x: x[1]))

    return max(pop, key=lambda chromosome: -fitness(chromosome, text))


def initpopulation(pop_size: int, chromosome_length: int, *,
                   random: Random) -> list[str]:
    return ["".join(random.choices(GENES, k=chromosome_length))
            for _ in range(pop_size)]


def selection(population: list[str], *,
              k: int = 3,
              fitness: Callable[[str], float],
              random: Random) -> list[str]:
    return tournament_selection(population,
                                k=k,
                                fitness=fitness,
                                random=random)


def tournament_selection(population: list[str], *,
                         k: int = 3,
                         fitness: Callable[[str], float],
                         random: Random) -> list[str]:
    selections = []
    for i in range(len(population)):
        chromosomes = random.sample(population, k=k)
        selected = max(chromosomes, key=fitness)
        selections.append(selected)
    return selections


def crossover(c1: str, c2: str, *, random: Random) -> tuple[str, str]:
    return uniform_crossover(c1, c2, random=random)


def uniform_crossover(p1: str, p2: str, *, random: Random) -> tuple[str, str]:
    mask = random.getrandbits(len(p1))
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


def mutate(chromosome: str, *, random: Random) -> str:
    return reciprocal_exchange_mutation(chromosome, random=random)


def reciprocal_exchange_mutation(chromosome: str, *, random: Random) -> str:
    i, j = random.sample(range(len(chromosome)), k=2)
    chars = list(chromosome)
    chars[i], chars[j] = chars[j], chars[i]
    return "".join(chars)


def fitness(chromosome: str, encrypted: str) -> float:
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

    # decrypt each character
    plain = [ord(i)-97 for i in decrypt(chromosome, encrypted)]

    # count the occurrences of each character
    counts = [0] * 26
    for i in plain:
        counts[i] += 1

    # calculate the total difference between the expected frequencies and actual frequencies
    score = 0.0
    for y in range(len(counts)):
        freq = counts[y] / len(plain)
        score += abs(freq - expected_frequencies[y])

    return score


def decrypt(chromosome: str, encrypted: str) -> str:
    # sanitize cipher text and key
    cipher = encrypted.lower()
    cipher = cipher.replace(r"[^a-z]", "")
    cipher = cipher.replace(r"\s", "")
    cipher = [ord(c) for c in cipher]

    key = chromosome.lower()
    key = key.replace(r"[^a-z]", "")
    key = key.replace(r"\s", "")
    key = [ord(c) - 97 for c in key]

    # decrypt each character
    plain = []
    key_ptr = 0
    for c in cipher:
        key_char = 0
        if len(key) > 0:
            # ignore any value not in the expected range
            while key[key_ptr] > 25 or key[key_ptr] < 0:
                key_ptr = (key_ptr + 1) % len(key)

            key_char = key[key_ptr]
            key_ptr = (key_ptr + 1) % len(key)

        plain.append(chr((26 + c - 97 - key_char) % 26 + 97))

    return "".join(i for i in plain)
