import abc
import sys
from io import TextIOBase
import pprint
import csv
from tabulate import tabulate

from . import Parameters


# (run, generation, best solution, best fitness, average fitness, file, seed, parameters, crossover, mutation, selection)
Row = tuple[int, int, str, float, float, str, int, Parameters, str, str, str]


class Printer(abc.ABC):
    @ abc.abstractmethod
    def __call__(self, rows: list[Row]) -> str:
        pass


class SimplePrinter(Printer):
    def __init__(self, stream: TextIOBase | None = None):
        self.stream = stream or sys.stdout

    def __call__(self, rows: list[Row]) -> None:
        for row in rows:
            print(row[0], row[1], row[2], row[3], file=self.stream)


class PrettyPrintPrinter(Printer):
    def __init__(self, stream: TextIOBase | None = None):
        self.stream = stream or sys.stdout

    def __call__(self, rows: list[Row]) -> None:
        for row in rows:
            obj = dict(
                solution=row[2],
                params=row[7],
                crossover=row[8],
                mutation=row[9],
                selection=row[10])
            pprint.pprint(obj, stream=self.stream)


class CsvPrinter(Printer):
    def __init__(self, stream: TextIOBase | None = None):
        self.stream = stream or sys.stdout
        self.headers = [
            "Run",
            "Generation",
            "File",
            "Seed",
            "Key Length",
            "Pop. Size",
            "Crossover Rate",
            "Mutation Rate",
            "Crossover",
            "Mutation",
            "Selection",
            "Best Solution",
            "Best Fitness",
            "Average Fitness",
        ]

    def __call__(self, rows: list[Row]) -> None:
        self.writer = csv.writer(self.stream, delimiter=",")
        self.writer.writerow(self.headers)

        rows = [
            (run,
             gen,
             file,
             seed,
             params.chromosome_length,
             params.initial_population_size,
             params.crossover_rate,
             params.mutation_rate,
             crossover,
             mutation,
             selection,
             solution,
             fitness,
             avg_fit,
             )
            for (run, gen, solution, fitness, avg_fit, file, seed, params, crossover, mutation, selection) in rows]
        self.writer.writerows(rows)


class TablePrinter(Printer):
    def __init__(self, stream: TextIOBase | None = None):
        self.stream = stream or sys.stdout
        self.headers = [
            "Run",
            "Generation",
            "File",
            "Seed",
            "Key Length",
            "Pop. Size",
            "Crossover Rate",
            "Mutation Rate",
            "Crossover",
            "Mutation",
            "Selection",
            "Solution",
            "Fitness",
            "Average Fitness",
        ]

    def _row(self, row: Row) -> tuple:
        run, gen, sol, fit, avgfit, file, seed, params, crossover, mutation, selection = row
        return (
            run,
            gen,
            file,
            seed,
            params.chromosome_length,
            params.initial_population_size,
            params.crossover_rate,
            params.mutation_rate,
            crossover,
            mutation,
            selection,
            sol,
            fit,
            avgfit)

    def __call__(self, rows: list[Row]) -> None:
        table = [self._row(row) for row in rows]
        print(tabulate(table, headers=self.headers))
