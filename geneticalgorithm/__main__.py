import sys
import argparse
import pathlib
from random import Random

from . import genetic_algorithm, Parameters
from .mutations import Mutation, ReciprocalExchangeMutation
from .crossovers import Crossover, UniformCrossover
from .selections import Selection, TournamentSelection
from .evaluators import ExpectedCharFrequencyEvaluator

parser = argparse.ArgumentParser(
    prog="Genetic Algorithm",
    description="performs genetic algorithm")

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
    "-c", "--crossover-rate",
    dest="crossover_rate",
    help="Crossover rate [default: 0.5]",
    type=float,
    default=0.5)
parser.add_argument(
    "--crossover-alg",
    dest="crossover_alg",
    help="""Crossover algorithm: [default: ux]
    ux - Uniform crossover
    """,
    type=str,
    choices=("ux",),
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
    help="""Selection algorithm: [default: tour]
    tour - Tournament selection
    """,
    type=str,
    choices=("tour",),
    default="tour")
parser.add_argument(
    "-m", "--mutation-rate",
    dest="mutation_rate",
    help="Mutation rate [default: 0.5]",
    type=float,
    default=0.5)
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
    if alg == "ux":
        return UniformCrossover(random=random)
    else:
        return UniformCrossover(random=random)


def selection_algorithm(alg: str, random: Random) -> Selection:
    if alg == "tour":
        return TournamentSelection(k=2, random=random)
    else:
        return TournamentSelection(k=2, random=random)


def main() -> int:
    args = parser.parse_args()

    if args.filepath is not None:
        with open(args.filepath) as f:
            text = f.read()
    else:
        text = "".join(sys.stdin)

    rng = Random(args.random_seed)

    params = Parameters(
        chromosome_length=args.key_length,
        initial_population_size=args.initial_population_size,
        max_generation_span=args.max_generations,
        crossover_rate=args.crossover_rate,
        mutation_rate=args.mutation_rate)

    solution = genetic_algorithm(
        params,
        crossover=crossover_algorithm(args.crossover_alg, random=rng),
        mutation=mutation_algorithm(args.mutation_alg, random=rng),
        selection=selection_algorithm(args.selection_alg, random=rng),
        fitness=ExpectedCharFrequencyEvaluator(text),
        rng=rng)

    print(solution)
    return 0


if __name__ == "__main__":
    sys.exit(main())
