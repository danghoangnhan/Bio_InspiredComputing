from abc import ABC
from collections import namedtuple
from typing import List
from ga.Task import Task

Genome = List[int]

Thing = namedtuple('Thing', ['name', 'value', 'weight'])

first_example = [
    Thing('Laptop', 500, 2200),
    Thing('Headphones', 150, 160),
    Thing('Coffee Mug', 60, 350),
    Thing('Notepad', 40, 333),
    Thing('Water Bottle', 30, 192),
]
second_example = [
                     Thing('Mints', 5, 25),
                     Thing('Socks', 10, 38),
                     Thing('Tissues', 15, 80),
                     Thing('Phone', 500, 200),
                     Thing('Baseball Cap', 100, 70)
                 ] + first_example


class Knapsack(Task, ABC):
    def __init__(self, fileName):

        self.priceWeightLineNumbers: list[int] = []
        self.prices: list[int] = []
        self.weights: list[int] = []
        self.weightedPrices: list[float] = []

        self.parseFile(fileName)

    def generate_things(self, num: int) -> [Thing]:
        return [Thing(f"thing{i}", i, i) for i in range(1, num + 1)]

    def fitness(self, genome: Genome, things: [Thing], weight_limit: int) -> int:
        if len(genome) != len(things):
            raise ValueError("genome and things must be of same length")

        weight = 0
        value = 0
        for i, thing in enumerate(things):
            if genome[i] == 1:
                weight += thing.weight
                value += thing.value

                if weight > weight_limit:
                    return 0

        return value

    def from_genome(self, genome: Genome, things: [Thing]) -> [Thing]:
        result = []
        for i, thing in enumerate(things):
            if genome[i] == 1:
                result += [thing]

        return result

    def to_string(self, things: [Thing]):
        return f"[{', '.join([t.name for t in things])}]"

    def value(self, things: [Thing]):
        return sum([t.value for t in things])

    def weight(self, things: [Thing]):
        return sum([p.weight for p in things])

    def print_stats(self, things: [Thing]):
        print(f"Things: {self.to_string(things)}")
        print(f"Value {self.value(things)}")
        print(f"Weight: {self.weight(things)}")

    def parseFile(self, fileName: str):
        with open(fileName) as file:
            index = [int(x) for x in file.read().split()]
            self.dimension = index[0]
            self.capacity = index[1]

            self.priceWeightLineNumbers = [i for i in range(self.dimension)]

            currentIndex: int = 0
            for j in range(2, len(index), 2):
                print(currentIndex, " ", j, '\n')
                self.weights.append(index[j])
                self.prices.append(index[j + 1])
                self.weightedPrices.append(self.prices[currentIndex] * 1.0 / self.weights[currentIndex])
                currentIndex += 1

        for i in range(self.dimension - 1):
            for j in range(i + 1, self.dimension, 1):
                if self.weightedPrices[i] > self.weightedPrices[j]:
                    self.weightedPrices[i], self.weightedPrices[j] = self.weightedPrices[j], self.weightedPrices[i]
                    self.priceWeightLineNumbers[i], self.priceWeightLineNumbers[j] = self.priceWeightLineNumbers[j], \
                                                                                     self.priceWeightLineNumbers[i]
