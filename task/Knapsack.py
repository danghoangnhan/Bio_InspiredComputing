import copy
from abc import ABC
from collections import namedtuple
from typing import List

import numpy as np

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
        self.parseFile(fileName)
        self.stride = 0
        self.window = np.random.uniform(0, 1,4)
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

            self.priceWeightLineNumbers = np.array([i for i in range(self.dimension)])
            self.weights = np.empty(self.dimension, dtype=float, order='C')
            self.prices = np.empty(self.dimension, dtype=float, order='C')
            self.weightedPrices = np.empty(self.dimension, dtype=float, order='C')

            currentIndex: int = 0

            for j in range(2, len(index), 2):
                self.weights[currentIndex] = index[j]
                self.prices[currentIndex] = index[j + 1]
                currentIndex += 1

        self.weightedPrices = self.prices * 1.0 / self.weights

        for i in range(self.dimension - 1):
            for j in range(i + 1, self.dimension, 1):
                if self.weightedPrices[i] > self.weightedPrices[j]:
                    self.weightedPrices[i], self.weightedPrices[j] = self.weightedPrices[j], \
                                                                     self.weightedPrices[i]
                    self.priceWeightLineNumbers[i], self.priceWeightLineNumbers[j] = \
                        self.priceWeightLineNumbers[j], \
                        self.priceWeightLineNumbers[i]

    def checkIndividualVail(self, ind):
        x = self.decode(ind)
        res = np.sum(np.multiply(self.weights, x))
        return res > self.capacity

    def decode(self, x):
        tmp_x = np.ndarray.copy(x)
        kp = []
        if len(tmp_x) > self.dimension:
            stride = self.getStride(x, tmp_x, self.window)

            for i in range(0, tmp_x.size(), stride):
                tmp: float = sum([tmp_x[i + j] * self.window[j] for j in range(self.window.length)])
                if tmp > 1:
                    tmp /= 10
                kp.append((int(round(tmp))))
        else:
            kp = np.round(tmp_x, 0)
        return kp

    def makeIndividualVail(self, x):
        x_decode = self.decode(x)
        wx: float = self.getWeight(x)
        i: int = 0
        if x.shape[0] > self.dimension:
            while wx > self.capacity:
                if x_decode[self.priceWeightLineNumbers[i]] == 1:
                    wx = wx - self.weights[self.priceWeightLineNumbers[i]]
                    for k in range(self.window.shape[0]):
                        x.set(self.priceWeightLineNumbers[i] * self.stride + k, 0.5 / (self.window.shape[0] * self.windowMax()))
                i += 1
        else:
            while wx > self.capacity:
                if x_decode[self.priceWeightLineNumbers[i]] == 1:
                    wx -= self.weights[self.priceWeightLineNumbers[i]]
                    x[self.priceWeightLineNumbers[i]] = x[self.priceWeightLineNumbers[i]] - 0.5
                i += 1

    def getWeight(self, ind):
        x = self.decode(ind)
        res = np.sum(np.multiply(self.weights,x))
        return res

    def windowMax(self):
        maxWindow:float = -1
        for window in range(self.window):
            if window > maxWindow:
                maxWindow = window
        maxWindow = np.amax(self.window)
        return max

    def computeFitness(self,ind):
        x = self.decode(ind)
        res = 0 - np.sum(np.multiply(self.prices, x))
        return res