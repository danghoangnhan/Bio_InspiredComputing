from random import randrange, random, uniform

from typing import List

import numpy as np

from ga.Population import Population
from ga.Task import Task
from ga.Individual import Individual


class MFEA:
    def __init__(self,
                 tasks: List[Task],
                 numOfInd: int,
                 pOfMutation: float,
                 timeResetPopulation: int,
                 ITERATION: int = 1000,
                 LIMIT: int = 10000000000):

        self.tasks = tasks
        self.timeResetPopulation = timeResetPopulation
        self.pOfMutation = pOfMutation
        self.population = Population(numOfInd, self.tasks)
        self.ITERATION: float = ITERATION
        self.LIMIT: int = LIMIT

    def run(self, nN: int):
        self.population.init()
        bestSolution: list = [self.population.individuals[i] for i in range(len(self.tasks))]
        changeBest: int = 0

        for i in range(self.ITERATION):
            for ii in range(len(self.tasks)):
                ind: Individual = self.population.getIndividualBestOfTask(ii)
                if bestSolution[ii].fitnessTask[ii] > ind.fitnessTask[ii]:
                    changeBest = 0
                    bestSolution[ii] = ind
                print(i, ":", ii, ": ", ind.fitnessTask)

            changeBest += 1

            if changeBest >= self.timeResetPopulation:
                self.population.init()
                changeBest = 0

            individuals: list[Individual] = self.population.individuals
            children: list[Individual] = []

            for j in range(nN):
                a: Individual = individuals[randrange(len(individuals))]
                b: Individual = individuals[randrange(len(individuals))]

                while a == b:
                    b = individuals[(randrange(len(individuals)))]

                t: float = uniform(0, 1)

                if (a.skillFactor == b.skillFactor) or (t > self.pOfMutation):
                    children += self.crossOver(a, b)
                else:
                    ia: Individual = self.mutation(a)
                    ib: Individual = self.mutation(b)
                    children.append(ia)
                    children.append(ib)

            self.population.add(children)
            self.selection()
            self.reComputeFitnessTaskForChild(children)
            self.population.updateRankPopulation()

        print("Solution:")
        for solution in bestSolution:
            print(solution.gen,"\n")
    def mutation(self, a: Individual) -> Individual:
        fR: list[int] = [(len(self.population.individuals) + 1) for _ in range(len(self.tasks))]

        t: int = randrange(len(a.gen))
        c = np.copy(a.gen)
        c[t] = uniform(0, 1)

        if self.population.checkIndividualVail(c):
            self.population.makeIndividualVail(c)

        ind: Individual = Individual(c, None)

        ind.skillFactor = a.skillFactor

        fitnessTa: list[float] = [self.LIMIT if i != ind.skillFactor else self.tasks[i].computeFitness(c)
                                  for i in range(len(self.tasks))]

        ind.fitnessTask = fitnessTa
        ind.factorial_rank = fR

        return ind

    def crossOver(self, a, b) -> List[Individual]:

        children: list[Individual] = []
        fR: list[int] = [(len(self.population.individuals) + 1) for _ in range(len(self.tasks))]

        t: int = randrange(len(a.gen) - 1)

        cb = np.concatenate([b.gen[0:t], a.gen[t:len(a.gen - 1)]])
        ca = np.concatenate([a.gen[0:t], b.gen[t:len(b.gen - 1)]])

        if self.population.checkIndividualVail(ca):
            self.population.makeIndividualVail(ca)

        ind1 = Individual(ca, None)
        rand: float = uniform(0, 1)

        ind1.skillFactor = a.skillFactor if rand < 0.5 else b.skillFactor

        fitnessTa = [self.LIMIT if i != ind1.skillFactor else self.tasks[i].computeFitness(ca)
                     for i in range(len(self.tasks))]

        ind1.fitnessTask = fitnessTa
        ind1.factorial_rank = fR
        children.append(ind1)

        if self.population.checkIndividualVail(cb):
            self.population.makeIndividualVail(cb)

        ind2 = Individual(cb, None)
        rand: float = uniform(0, 1)

        ind2.skillFactor = a.skillFactor if rand < 0.5 else b.skillFactor

        fitnessTa: list[float] = [self.LIMIT if i != ind2.skillFactor else self.tasks[i].computeFitness(cb)
                                  for i in range(len(self.tasks))]

        ind2.fitnessTask = fitnessTa
        ind2.factorial_rank = fR
        children.append(ind2)

        return children

    def selection(self):
        # sort list by `individuals` in the natural order
        self.population.individuals.sort(key=lambda individual: individual.scalarFitness)
        newIndividuals: List[Individual] = [self.population.individuals[i] for i in range(self.population.nIndividual)]
        self.population.individuals = newIndividuals

    def reComputeFitnessTaskForChild(self, children: List[Individual]):

        for child in children:
            fT: List[float] = child.fitnessTask
            for j in range(len(self.tasks)):
                if fT[j] == self.LIMIT:
                    t: Task = self.tasks[j]
                    fT[j] = t.computeFitness(child.gen)
