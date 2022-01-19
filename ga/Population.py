import copy
import operator
import random
from typing import List

import numpy as np

from ga.Individual import Individual
from ga.Task import Task


class Population(Task):
    def __init__(self, n: int, tasks: List[Task]):
        self.nIndividual: int = n
        self.nTask: int = len(tasks)
        self.tasks: list[Task] = tasks
        self.individuals = None
        maxDimension: int = max(self.tasks, key=lambda task: task.dimension).dimension
        minDimension: int = min(self.tasks, key=lambda task: task.dimension).dimension

        self.lenGen = maxDimension

    def init(self):
        self.individuals: list = []

        for i in range(self.nIndividual):
            g: List[float] = np.random.uniform(0, 1, self.lenGen)

            if self.checkIndividualVail(g):
                self.makeIndividualVail(g)

            fitnessTa: List[float] = [task.computeFitness(g) for task in self.tasks]
            self.individuals.append(Individual(g, fitnessTa))

        self.updateRankPopulation()

    def checkIndividualVail(self, ind) -> bool:
        result = any([task.checkIndividualVail(ind) for task in self.tasks])
        return result

    def makeIndividualVail(self, genome: List[float]):
        xd: int = 0
        while xd < len(self.tasks):
            for task in self.tasks:
                if task.checkIndividualVail(genome):
                    xd = 0
                    task.makeIndividualVail(genome)
                else:
                    xd += 1

    def updateRankPopulation(self):
        rankInTask: List[Individual] = [[] for _ in range(0, self.nTask, 1)]

        for ind in self.individuals:
            for i in range(self.nTask):
                lstIndividualInTask: list[Individual] = rankInTask[i]
                check: bool = True
                for j in range(len(lstIndividualInTask)):
                    if lstIndividualInTask[j].fitnessTask[i] > ind.fitnessTask[i]:
                        lstIndividualInTask.insert(j, ind)
                        check = False
                        break
                if check:
                    lstIndividualInTask.append(ind)
                rankInTask[i] = lstIndividualInTask

        for indIndex, ind in enumerate(self.individuals):
            factorial_rank: list[int] = []
            min_rank: int = self.nIndividual + 2
            task_rank_min: int = -1

            for j, task in enumerate(rankInTask):
                rankJ: int = task.index(ind) + 1
                factorial_rank.append(task.index(ind) + 1)
                if rankJ < min_rank:
                    min_rank = rankJ
                    task_rank_min = j
            factorial_rank1: list[int] = [task.index(ind) + 1 for task in rankInTask]
            min_index, min_value = min([(index, value) for index, value in enumerate(factorial_rank1)])
            ind.factorial_rank = factorial_rank
            ind.skillFactor = task_rank_min
            ind.scalarFitness = 1.0 / min_rank

    def getIndividualBestOfTask(self, task):
        best = min(self.individuals, key=lambda individual: individual.factorial_rank[task])
        return best

    def add(self, offsprings: List[Individual]):

        self.individuals += offsprings

        for offspringIndex, offspring in enumerate(offsprings):
            child: Individual = offspring
            rankInTask = self.countRank(child.skillFactor)
            index = next(idx for idx, rankInTask in enumerate(rankInTask)
                         if rankInTask.fitnessTask[child.skillFactor] > child.fitnessTask[child.skillFactor])
            if index > -1:
                for tmpIndividual in rankInTask[index:]:
                    rank = tmpIndividual.factorial_rank
                    rank[child.skillFactor] += 1
                    tmpIndividual.factorial_rank = rank
            else:
                index = len(rankInTask)
            facRankInd = [len(self.individuals) + 1 for _ in range(self.nTask)]

            facRankInd[child.skillFactor] = index + 1
            child.setFactorial_rank = facRankInd
            offsprings[offspringIndex] = child

        for ind in offsprings:
            ind.scalarFitness = 1 / ind.getMinFactorialRank()

    def countRank(self, task: int) -> List[Individual]:
        lstIndividualInTask: List[Individual] = []
        for ind in self.individuals:
            check: bool = True
            for j in range(len(lstIndividualInTask)):
                if lstIndividualInTask[j].fitnessTask[task] > ind.fitnessTask[task]:
                    lstIndividualInTask.insert(j, ind)
                    check = False
                    break
            if check:
                lstIndividualInTask.append(ind)
        return lstIndividualInTask
