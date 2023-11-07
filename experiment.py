import sys
import argparse
import pathlib
from random import Random
from pprint import pprint

from geneticalgorithm import genetic_algorithm, Parameters
from geneticalgorithm.mutations import Mutation, ReciprocalExchangeMutation
from geneticalgorithm.crossovers import Crossover, UniformCrossover, OrderCrossover
from geneticalgorithm.evaluators import ExpectedCharFrequencyEvaluator
from geneticalgorithm.selections import (
    Selection,
    TournamentSelection,
    WithElitism
)


parser = argparse.ArgumentParser(
    prog="GA Experiment",
    description="performs genetic algorithm experiment")

parser.add_argument(
    "key_length",
    help="Maximum length of key",
    type=int)

parser.add_argument(
    "-f", "--file",
    dest="filepath",
    help="filepath to the encrypted data. [default: read from stdin]",
    type=pathlib.Path)
parser.add_argument(
    "--crossover-alg",
    dest="crossover_alg",
    help="""Crossover algorithm: [default: ux]
    ux - Uniform crossover
    ox - Order crossover
    """,
    type=str,
    choices=("ux", "ox"),
    default="ux")
parser.add_argument(
    "--mutation-alg",
    dest="mutation_alg",
    help="""Mutation algorithm: [default: rx]
    rx - Reciprocal Exchange
    """,
    type=str,
    choices=("rx",),
    default="rx")
parser.add_argument(
    "--selection-alg",
    dest="selection_alg",
    help="""Selection algorithm: [default: tour2]
    tour{k} - Tournament selection
    """,
    type=str,
    choices=("tour2", "tour3", "tour4", "tour5"),
    default="tour2")
parser.add_argument(
    "-p", "--population-size",
    dest="initial_population_size",
    help="Initial population size [default: 50]",
    type=int,
    default=50)
parser.add_argument(
    "-g", "--max-generations",
    dest="max_generations",
    help="Maximum number of generations [default: 20]",
    type=int,
    default=20)
parser.add_argument(
    "--elites",
    dest="n_elites",
    help="""Number of elites to preserve each generation [default: 3]
     set `--elites=0` to disable elitism
    """,
    type=int,
    default=5)
parser.add_argument(
    "-s", "--seed",
    dest="random_seed",
    help="Random seed for reproducibility [default: None]",
    type=int)


def mutation_algorithm(alg: str, random: Random) -> Mutation:
    if alg == "rx":
        return ReciprocalExchangeMutation(random=random)
    else:
        return ReciprocalExchangeMutation(random=random)


def crossover_algorithm(alg: str, random: Random) -> Crossover:
    if alg == "ox":
        return OrderCrossover(random=random)
    else:
        return UniformCrossover(random=random)


def selection_algorithm(alg: str, random: Random) -> Selection:
    if alg.startswith("tour"):
        k = int(alg.replace("tour", ""))
        return TournamentSelection(k=k, random=random)
    else:
        return TournamentSelection(k=2, random=random)


CONFIGS = [
    dict(crossover=1.0, mutation=0.0),
    dict(crossover=1.0, mutation=0.1),
    dict(crossover=0.9, mutation=0.0),
    dict(crossover=0.9, mutation=0.1),
]


def main() -> int:
    args = parser.parse_args()

    if args.filepath is not None:
        with open(args.filepath) as f:
            text = f.read()
    else:
        text = "".join(sys.stdin)

    results = []
    for config in CONFIGS:
        rng = Random(args.random_seed)

        params = Parameters(
            chromosome_length=args.key_length,
            initial_population_size=args.initial_population_size,
            max_generation_span=args.max_generations,
            crossover_rate=config["crossover"],
            mutation_rate=config["mutation"])

        selection = WithElitism(
            selection_algorithm(args.selection_alg, random=rng),
            random=rng,
            n_elites=args.n_elites)

        solution = genetic_algorithm(
            params,
            crossover=crossover_algorithm(args.crossover_alg, random=rng),
            mutation=mutation_algorithm(args.mutation_alg, random=rng),
            selection=selection,
            fitness=ExpectedCharFrequencyEvaluator(text),
            rng=rng)

        results.append((params, solution))

    pprint(results)
    return 0


if __name__ == "__main__":
    sys.exit(main())
