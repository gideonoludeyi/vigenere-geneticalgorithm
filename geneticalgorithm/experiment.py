import sys
import argparse
import pathlib
import json
import contextlib
from io import TextIOBase
from random import Random
from itertools import product

from . import genetic_algorithm, Parameters, ALLELES
from .mutations import (
    Mutation,
    ReciprocalExchangeMutation,
    RandomCharacterMutation
)
from .crossovers import (
    Crossover,
    UniformCrossover,
    OrderCrossover
)
from .evaluators import ExpectedCharFrequencyEvaluator
from .selections import (
    Selection,
    TournamentSelection,
    WithElitism
)
from .printers import (
    Printer,
    SimplePrinter,
    PrettyPrintPrinter,
    CsvPrinter,
    TablePrinter
)
from .utils import decrypt

try:
    from tqdm import tqdm
except ImportError:
    print("To see progress bar, install tqdm package", file=sys.stderr)

    def tqdm(*args, **kwargs):
        return contextlib.nullcontext()

parser = argparse.ArgumentParser(
    prog="GA Experiment",
    description="performs genetic algorithm experiment")

parser.add_argument(
    "config",
    help="Path to configuration file for experiment runs",
    type=pathlib.Path)
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
    "-v", "--verbose",
    dest="verbose",
    help="Whether to output all logs",
    action="store_true",
    default=False)


def mutation_algorithm(alg: str, random: Random) -> Mutation:
    if alg == "rc":
        return RandomCharacterMutation(alleles=ALLELES, random=random)
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


def output_printer(output_format: str,
                   stream: TextIOBase = sys.stdout) -> Printer:
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

    with open(args.config) as f:
        config = json.load(f)

    printer = output_printer(args.output_format, sys.stdout)

    steps = sum(
        len(config["seeds"]) * len(run["rates"]) *
        config["max_gen"] * len(run["crossover_algorithms"]) *
        len(run["mutation_algorithms"]) * len(run["selection_algorithms"])
        for run in config["runs"])

    results = []
    with tqdm(total=steps, ascii=True, leave=False) as progress:
        run = 1
        for spec in config["runs"]:
            with open(spec["file"]) as f:
                text = f.read()

            it = product(
                config["seeds"],
                spec["crossover_algorithms"],
                spec["mutation_algorithms"],
                spec["selection_algorithms"],
                spec["rates"])
            for seed, crossover_alg, mutation_alg, selection_alg, rate in it:
                rng = Random(seed)
                params = Parameters(
                    chromosome_length=spec["key_length"],
                    initial_population_size=config["pop_size"],
                    max_generation_span=config["max_gen"],
                    crossover_rate=rate["crossover"],
                    mutation_rate=rate["mutation"])

                crossover = crossover_algorithm(crossover_alg, random=rng)
                mutation = mutation_algorithm(mutation_alg, random=rng)
                selection = WithElitism(
                    selection_algorithm(selection_alg, random=rng),
                    random=rng,
                    n_elites=config["elites"])

                if args.verbose:
                    print(dict(
                        random_seed=seed,
                        crossover=crossover,
                        datafile=spec["file"],
                        crossover_rate=params.crossover_rate,
                        mutation_rate=params.mutation_rate,
                        n_chromosomes=params.initial_population_size,
                        chromosome_max_length=params.chromosome_length,
                        max_generation_span=params.max_generation_span,
                    ))

                g = genetic_algorithm(
                    params,
                    crossover=crossover,
                    mutation=mutation,
                    selection=selection,
                    fitness=ExpectedCharFrequencyEvaluator(text),
                    rng=rng,
                    verbose=args.verbose)

                fitnesses = dict()
                for gen, fitnesses in enumerate(g, 1):
                    if progress is not None:
                        progress.update(1)

                    solution, fitness = max(fitnesses.items(),
                                            key=lambda tup: -tup[1])
                    avg_fitness = (sum(fitnesses.values()) /
                                   len(fitnesses.values()))
                    results.append((
                        run,
                        gen,
                        solution,
                        fitness,
                        avg_fitness,
                        spec["file"],
                        seed,
                        params,
                        crossover_alg,
                        mutation_alg,
                        selection_alg))

                if args.verbose:
                    solution, fitness = max(fitnesses.items(),
                                            key=lambda tup: -tup[1])
                    print(
                        dict(
                            solution=solution,
                            fitness=fitness,
                            decrypted=decrypt(solution, text)),
                        end="\n\n")

                run += 1

    printer(results)

    return 0


if __name__ == "__main__":
    sys.exit(main())
