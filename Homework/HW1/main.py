import math
from copy import copy
import random
import ast
from ast import literal_eval
import numpy
import numpy as np
from matplotlib import pyplot as plt
from bitstring import BitArray


def bin2int(x):
    y = 0
    for i, j in enumerate(x):
        y += j << len(x) - 1 - i
    signedValue = y & 0xffffffff
    signedValue = y | (-(y & 0x80000000))
    return signedValue


class GA:
    def __init__(self, popn, num_gen, num_parent, GA_type):
        self.popn = popn
        self.num_gen = num_gen
        self.n_parents_mating = num_parent
        self.dim = self.popn.shape[1]
        self.GA_type = GA_type
    def fitnessFunc(self, chromosome):
        """F7 Schwefel's function
        multimodal, asymmetric, separable"""
        alpha = 418.982887
        fitness = 0
        for i in range(len(chromosome)):
            fitness -= chromosome[i] * math.sin(math.sqrt(math.fabs(chromosome[i])))
        return float(fitness) + alpha * len(chromosome)

    # Functions to use are rastrigins,shifted_sphere,shifted_schwefel,shifted_Griewanks,shifted_Rosenbrock,
    def calculate_fitness(self, currentPopulation):
        # Calculating the fitness value of each solution in the current population.
        if self.GA_type == "Bit_Strings":
            convertedFloatArray = []
            for row in currentPopulation:
                matrix = row.reshape(int(row.shape[0] / 10), 10)
                result = [bin2int(index[::-1]) for index in matrix]
                convertedFloatArray.append(result)
            return np.apply_along_axis(self.fitnessFunc, 1, convertedFloatArray)
        if self.GA_type == "Real_valued":
            if currentPopulation.ndim > 1:
                return np.apply_along_axis(self.fitnessFunc, 1, currentPopulation)
            else:
                return self.fitnessFunc(currentPopulation)

    def tournament(self, fitness, pop, num_parents):
        parents = numpy.empty((num_parents, pop.shape[1]))
        for parent_num in range(num_parents):
            fitness_idx = numpy.where(fitness == numpy.max(fitness))
            fitness_idx = np.argmax(fitness, axis=0)
            parents[parent_num, :] = pop[fitness_idx, :]
            fitness[fitness_idx] = float('-inf')
        return parents

    def tournament_selection(self, population):
        parents = random.choices(population, k=2)
        parents = sorted(parents, key=lambda agent: self.calculate_fitness(agent), reverse=True)
        return parents[0]

    def two_point_crossover(self, parents, offspring_size, pc=0.9):
        offspring = np.empty(offspring_size)
        # Selecting the point at which crossover occurs between two parents.Normally it is at center.
        crossover_point1 = random.randint(0, parents.shape[1] - 1)
        crossover_point2 = random.randint(0, parents.shape[1] - 1)

        if crossover_point1 > crossover_point2:
            crossover_point1, crossover_point2 = crossover_point2, crossover_point1
        for idx in range(0, numpy.uint8(parents.shape[0] / 2), 2):
            # Index of the first parent to mate.
            parent1_idx = idx
            # Index of the second parent to mate.
            parent2_idx = idx + 1
            # The first offspring will have its middle half of its genes taken from the second parent.
            offspring[idx, 0:crossover_point1] = parents[parent1_idx, 0:crossover_point1]
            offspring[idx, crossover_point1:crossover_point2] = parents[parent2_idx, crossover_point1:crossover_point2]
            offspring[idx, crossover_point2:] = parents[parent1_idx, crossover_point2:]
            # The second offspring will have its middle half of its genes taken from the first parent.
            offspring[idx + 1, 0:crossover_point1] = parents[parent2_idx, 0:crossover_point1]
            offspring[idx + 1, crossover_point1:crossover_point2] = parents[parent1_idx,
                                                                    crossover_point1:crossover_point2]
            offspring[idx + 1, crossover_point2:] = parents[parent2_idx, crossover_point2:]
        return offspring

    def Uniform_Crossover(self, parents, offspring_size):
        offspring = np.empty(offspring_size)
        for parentIndex in range(0, numpy.uint8(parents.shape[0]), 2):
            for k in range(numpy.uint8(offspring_size[1])):
                offspring[parentIndex, k] = parents[parentIndex + random.randint(0, 1), k]
                offspring[parentIndex + 1, k] = parents[parentIndex + random.randint(0, 1), k]
        return offspring

    def arithmetic_recombination(self, parents, offspring_size):
        pm = 1 / offspring_size[1]
        offspring = np.empty(offspring_size)
        # Mutation changes a selected genes in each offspring randomly.
        for idx in range(0, parents.shape[0], 2):
            # The random value to be added to the gene.
            for k in range(numpy.uint8(offspring_size[1])):
                offspring[idx, k] = pm * parents[idx+1, k] + (1 - pm) * parents[idx, k]
                offspring[idx + 1, k] = pm * parents[idx, k] + (1 - pm) * parents[idx+1, k]
        return offspring

    def mutation(self, offspring_crossover):
        # Mutation changes a selected genes in each offspring randomly.
        for idx in range(offspring_crossover.shape[0]):
            # The random value to be added to the gene.
            random_value = numpy.random.uniform(-1.0, 1.0, 1)
            rand_idx = random.randint(0, offspring_crossover.shape[1] - 1)
            offspring_crossover[idx, rand_idx:] = offspring_crossover[idx, rand_idx:] - random_value
        return offspring_crossover

    def bitflipMutation(self, offspring_crossover):
        for idx in range(offspring_crossover.shape[0]):
            point = np.random.randint(len(offspring_crossover))
            offspring_crossover[point] = 1 - offspring_crossover[point]
        return offspring_crossover

    def start_opt_GA(self):
        Error = []
        Solution = []
        for generation in range(self.num_gen):
            fitness = self.calculate_fitness(self.popn)
            parents = self.tournament(fitness, self.popn, self.n_parents_mating)
            # Getting next generation by crossover.
            if self.GA_type == "Bit_Strings":
                offspring_crossover = self.two_point_crossover(parents, offspring_size=(
                    self.popn.shape[0] - parents.shape[0], self.dim))
                offspring_mutation = self.mutation(offspring_crossover)
            if self.GA_type == "Real_valued":
                offspring_crossover = self.arithmetic_recombination(parents, offspring_size=(
                    self.popn.shape[0] - parents.shape[0], self.dim))
                offspring_mutation = self.mutation(offspring_crossover)
            # Creating new population of offsprings
            self.popn[0:parents.shape[0], :] = parents
            self.popn[parents.shape[0]:, :] = offspring_mutation
            # The best result in the current generation.
            err = np.min(self.calculate_fitness(self.popn))
            sol = np.max(self.calculate_fitness(self.popn))
            Error.append(err)
            Solution.append(sol)
            print("Best result in generation {0} is {1}".format(generation, sol))
            # Getting the best solution in final generation.
        fitness = self.calculate_fitness(self.popn)
        # Return the index of the solution with the best fitness.
        best_match_idx = np.where(fitness == np.max(fitness))
        print("Best solution : ", self.popn[best_match_idx, :])
        print("Best solution fitness : ", fitness[best_match_idx])
        return Solution, Error


np.random.seed(59)
minBound = -512.0
maxBound = 512.0
realValuepopulation = np.random.uniform(low=minBound, high=maxBound, size=(100, 10))
bitStringPopulation = numpy.random.choice([0, 1], (100, 100), p=[0.9, 0.1])
populationSize = 100

print("Starting GA:")
num_generations = 500

Real_ValueGA = GA(copy(realValuepopulation), num_generations, 2, "Real_valued")
Bit_stringsGA = GA(copy(bitStringPopulation), num_generations, 2, "Bit_Strings")

Bit_stringGA_Sol, Bit_stringGA_Error = Bit_stringsGA.start_opt_GA()
Real_ValueGA_Sol, Real_ValueGA_Error = Real_ValueGA.start_opt_GA()

plt.semilogy(Bit_stringGA_Sol, color='red', label="Bit String GA Fitness")
plt.semilogy(Real_ValueGA_Sol, color='blue', label="Real Value GA Fitness")
plt.ylabel('Fitness Value')
plt.xlabel('Generations Number')
plt.legend(loc='best')
plt.show()
