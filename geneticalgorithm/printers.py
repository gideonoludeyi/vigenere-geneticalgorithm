import abc
import sys
from io import TextIOBase
import pprint
import csv
from tabulate import tabulate

from . import Parameters
from .crossovers import Crossover
from .mutations import Mutation
from .selections import Selection


# (solution, parameters, crossover, mutation, selection)
Row = tuple[str, Parameters, Crossover, Mutation, Selection]


class Printer(abc.ABC):
    @abc.abstractmethod
    def __call__(self, rows: list[Row]) -> str:
        pass


class SimplePrinter(Printer):
    def __init__(self, stream: TextIOBase | None = None):
        self.stream = stream or sys.stdout

    def __call__(self, rows: list[Row]) -> None:
        for row in rows:
            print(row[0], file=self.stream)


class PrettyPrintPrinter(Printer):
    def __init__(self, stream: TextIOBase | None = None):
        self.stream = stream or sys.stdout

    def __call__(self, rows: list[Row]) -> None:
        for row in rows:
            obj = dict(
                solution=row[0],
                params=row[1],
                crossover=row[2],
                mutation=row[3],
                selection=row[4])
            pprint.pprint(obj, stream=self.stream)


class CsvPrinter(Printer):
    def __init__(self, stream: TextIOBase | None = None):
        self.writer = csv.writer(stream or sys.stdout, delimiter="\t")
        self.writer.writerow([
            "Chromosome Length",
            "Initial Pop. Size",
            "Crossover Rate",
            "Mutation Rate",
            "Solution",
        ])

    def __call__(self, rows: list[Row]) -> None:
        for row in rows:
            solution, params, *_ = row
            self.writer.writerow((
                params.chromosome_length,
                params.initial_population_size,
                params.crossover_rate,
                params.mutation_rate,
                solution,
            ))


class TablePrinter(Printer):
    def __init__(self, stream: TextIOBase | None = None):
        self.stream = stream or sys.stdout

    def __call__(self, rows: list[Row]) -> None:
        headers = [
            "Chromosome Length",
            "Initial Pop. Size",
            "Crossover Rate",
            "Mutation Rate",
            "Solution",
        ]
        table = [
            (params.chromosome_length,
             params.initial_population_size,
             params.crossover_rate,
             params.mutation_rate,
             solution)
            for solution, params, crossover, mutation, selection in rows]

        print(tabulate(table, headers=headers))
