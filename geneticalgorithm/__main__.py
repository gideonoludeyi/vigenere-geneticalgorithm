import sys
import argparse
import pathlib
from random import Random

from . import genetic_algorithm, Parameters, ALLELES
from .mutations import (
    Mutation,
    ReciprocalExchangeMutation,
    RandomCharacterMutation
)
from .crossovers import Crossover, UniformCrossover, OrderCrossover
from .selections import Selection, TournamentSelection, WithElitism
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
    help="Crossover rate [default: 0.9]",
    type=float,
    default=0.9)
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
    rc - Random Character mutation
    """,
    type=str,
    choices=("rx", "rc"),
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
    help="Mutation rate [default: 0.1]",
    type=float,
    default=0.1)
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
    """selects the mutation algorithm to use
    based on provided CLI option
    """
    if alg == "rc":
        return RandomCharacterMutation(alleles=ALLELES, random=random)
    else:
        return ReciprocalExchangeMutation(random=random)


def crossover_algorithm(alg: str, random: Random) -> Crossover:
    """selects the crossover algorithm to use
    based on provided CLI option
    """
    if alg == "ox":
        return OrderCrossover(random=random)
    else:
        return UniformCrossover(random=random)


def selection_algorithm(alg: str, random: Random) -> Selection:
    """selects the selection algorithm to use
    based on provided CLI option
    """
    if alg.startswith("tour"):
        k = int(alg.replace("tour", ""))
        return TournamentSelection(k=k, random=random)
    else:
        return TournamentSelection(k=2, random=random)


def main() -> int:
    args = parser.parse_args()

    if args.filepath is not None:
        with open(args.filepath) as f:
            text = f.read().strip()
    else:
        text = "".join(sys.stdin).strip()

    rng = Random(args.random_seed)

    # construct parameters
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

    # create genetic algorithm iterator
    g = genetic_algorithm(
        params,
        crossover=crossover,
        mutation=mutation,
        selection=selection,
        # use default fitness function
        fitness=ExpectedCharFrequencyEvaluator(text),
        rng=rng)

    # run the GA and get all generation fitness values
    generations = list(g)
    # get the final set of fitness values
    final_generation_fitness_map = generations[-1]

    # get the best solution and fitness value from final generation
    solution, fitness = max(final_generation_fitness_map.items(),
                            key=lambda tup: -tup[1])

    print(f"Best Solution: {solution}")
    print(f"Best Fitness: {fitness}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
