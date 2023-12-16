import abc
from .utils import decrypt


class Evaluator(abc.ABC):
    """base class for evaluators"""

    @abc.abstractmethod
    def __call__(self, chromosome: str) -> float:
        pass


class ExpectedCharFrequencyEvaluator(Evaluator):
    """python implementation of fitness function provided in Evaluation.java"""

    def __init__(self, encrypted: str):
        self.encrypted = encrypted

    def __call__(self, chromosome: str) -> float:
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
        plain = [ord(i) - 97 for i in decrypt(chromosome, self.encrypted)]

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
