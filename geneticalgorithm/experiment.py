import sys
import argparse
import pathlib
import json
import contextlib
from io import TextIOBase
from random import Random
from itertools import product

from . import genetic_algorithm, Parameters, ALLELES
from .mutations import Mutation, ReciprocalExchangeMutation, RandomCharacterMutation
from .crossovers import Crossover, UniformCrossover, OrderCrossover
from .evaluators import ExpectedCharFrequencyEvaluator
from .selections import Selection, TournamentSelection, WithElitism
from .printers import (
    Printer,
    SimplePrinter,
    PrettyPrintPrinter,
    CsvPrinter,
    TablePrinter,
)
from .utils import decrypt

try:
    from tqdm import tqdm
except ImportError:
    print("To see progress bar, install tqdm package", file=sys.stderr)

    def tqdm(*args, **kwargs):
        return contextlib.nullcontext()


parser = argparse.ArgumentParser(
    prog="GA Experiment", description="performs genetic algorithm experiment"
)

parser.add_argument(
    "config", help="Path to configuration file for experiment runs", type=pathlib.Path
)
parser.add_argument(
    "-o",
    "--output-format",
    dest="output_format",
    help="""How to format output [default: simple]
      simple - SimplePrinter
      pp - PrettyPrintPrinter
      csv - CsvPrinter
      tbl - TablePrinter
    """,
    type=str,
    choices=("simple", "pp", "csv", "tbl"),
    default="simple",
)
parser.add_argument(
    "-v",
    "--verbose",
    dest="verbose",
    help="Whether to output all logs",
    action="store_true",
    default=False,
)


def mutation_algorithm(alg: str, random: Random) -> Mutation:
    """selects the mutation algorithm to use
    based on provided configuration value
    """
    if alg == "rc":
        return RandomCharacterMutation(alleles=ALLELES, random=random)
    else:
        return ReciprocalExchangeMutation(random=random)


def crossover_algorithm(alg: str, random: Random) -> Crossover:
    """selects the crossover algorithm to use
    based on provided configuration value
    """
    if alg == "ox":
        return OrderCrossover(random=random)
    else:
        return UniformCrossover(random=random)


def selection_algorithm(alg: str, random: Random) -> Selection:
    """selects the selection algorithm to use
    based on provided configuration value
    """
    if alg.startswith("tour"):
        k = int(alg.replace("tour", ""))
        return TournamentSelection(k=k, random=random)
    else:
        return TournamentSelection(k=2, random=random)


def output_printer(output_format: str, stream: TextIOBase = sys.stdout) -> Printer:
    """selects the output formatting implementation
    to display the results based on provided CLI option
    """
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

    # compute number of steps required for experiment
    # (for progress bar)
    steps = sum(
        len(config["seeds"])
        * len(run["rates"])
        * config["max_gen"]
        * len(run["crossover_algorithms"])
        * len(run["mutation_algorithms"])
        * len(run["selection_algorithms"])
        for run in config["runs"]
    )

    results = []  # list of data points (per generation)
    with tqdm(total=steps, ascii=True, leave=False) as progress:
        run = 1
        for spec in config["runs"]:
            with open(spec["file"]) as f:
                text = f.read()

            it = product(  # all combination of parameters
                config["seeds"],
                spec["crossover_algorithms"],
                spec["mutation_algorithms"],
                spec["selection_algorithms"],
                spec["rates"],
            )
            for seed, crossover_alg, mutation_alg, selection_alg, rate in it:
                rng = Random(seed)
                # construct parameters
                params = Parameters(
                    chromosome_length=spec["key_length"],
                    initial_population_size=config["pop_size"],
                    max_generation_span=config["max_gen"],
                    crossover_rate=rate["crossover"],
                    mutation_rate=rate["mutation"],
                )

                crossover = crossover_algorithm(crossover_alg, random=rng)
                mutation = mutation_algorithm(mutation_alg, random=rng)
                selection = WithElitism(
                    selection_algorithm(selection_alg, random=rng),
                    random=rng,
                    n_elites=config["elites"],
                )

                # create genetic algorithm iterator
                g = genetic_algorithm(
                    params,
                    crossover=crossover,
                    mutation=mutation,
                    selection=selection,
                    # use default fitness function
                    fitness=ExpectedCharFrequencyEvaluator(text),
                    rng=rng,
                )

                fitnesses = dict()
                for gen, fitnesses in enumerate(g, 1):
                    if progress is not None:
                        progress.update(1)

                    best_solution, best_fit = max(
                        fitnesses.items(), key=lambda tup: -tup[1]
                    )
                    avg_fitness = sum(fitnesses.values()) / len(fitnesses.values())
                    # add run result to result dataset
                    results.append(
                        (
                            run,
                            gen,
                            best_solution,
                            best_fit,
                            avg_fitness,
                            spec["file"],
                            seed,
                            params,
                            crossover_alg,
                            mutation_alg,
                            selection_alg,
                        )
                    )

                # display solution and decrypted cipher each run
                if args.verbose:
                    best_solution, best_fit = max(
                        fitnesses.items(), key=lambda tup: -tup[1]
                    )
                    print(
                        dict(
                            solution=best_solution,
                            fitness=best_fit,
                            decrypted=decrypt(best_solution, text),
                        ),
                        end="\n\n",
                    )

                run += 1

    # output results in user-specified format
    printer(results)

    return 0


if __name__ == "__main__":
    sys.exit(main())
