import sys
import argparse
import pathlib
from io import TextIOBase
from random import Random

from . import genetic_algorithm, Parameters
from .mutations import Mutation, ReciprocalExchangeMutation
from .crossovers import Crossover, UniformCrossover, OrderCrossover
from .selections import Selection, TournamentSelection, WithElitism
from .evaluators import ExpectedCharFrequencyEvaluator
from .printers import (
    Printer,
    SimplePrinter,
    PrettyPrintPrinter,
    CsvPrinter,
    TablePrinter
)

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
    "-o", "--output-format",
    dest="output_format",
    help="""How to format output [default: simple]
      simple - SimplePrinter
      pp - PrettyPrintPrinter
      csv - CsvPrinter
      tbl - TablePrinter
    """,
    type=str,
    choices=("simple", "pp", "csv", "tbl"),
    default="simple")
parser.add_argument(
    "--elites",
    dest="n_elites",
    help="""Number of elites to preserve each generation [default: 2]
     set `--elites=0` to disable elitism
    """,
    type=int,
    default=2)
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


def output_printer(output_format: str, stream: TextIOBase = sys.stdout) -> Printer:
    if output_format == "pp":
        return PrettyPrintPrinter(stream)
    elif output_format == "csv":
        return CsvPrinter(stream)
    elif output_format == "tbl":
        return TablePrinter(stream)
    else:
        return SimplePrinter(stream)


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

    crossover = crossover_algorithm(args.crossover_alg, random=rng)
    mutation = mutation_algorithm(args.mutation_alg, random=rng)

    selection = WithElitism(
        selection_algorithm(args.selection_alg, random=rng),
        random=rng,
        n_elites=args.n_elites)

    g = genetic_algorithm(
        params,
        crossover=crossover,
        mutation=mutation,
        selection=selection,
        fitness=ExpectedCharFrequencyEvaluator(text),
        rng=rng)

    generations = list(g)
    final_generation_fitness_map = generations[-1]
    solution, fitness = max(final_generation_fitness_map.items(),
                            key=lambda tup: -tup[1])

    print(f"Best Solution: {solution}")
    print(f"Best Fitness: {fitness}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
