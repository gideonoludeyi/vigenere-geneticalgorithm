import sys
import argparse
import pathlib

from .algorithm import genetic_algorithm, Parameters

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


def main():
    args = parser.parse_args()

    if args.filepath is not None:
        with open(args.filepath) as f:
            text = f.read()
    else:
        text = "".join(sys.stdin)

    params = Parameters(
        chromosome_length=args.key_length,
        initial_population_size=args.initial_population_size,
        max_generation_span=args.max_generations,
        crossover_rate=args.crossover_rate,
        mutation_rate=args.mutation_rate,
        random_seed=args.random_seed)

    solution = genetic_algorithm(text, params)

    print(solution)


if __name__ == "__main__":
    main()
