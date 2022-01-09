import sys
from random import random

from typing import List

from ga.Individual import Individual
from Task import Task


class Population:
    individuals: list[Individual]

    def __init__(self, n: int, tasks: list[Task]):
        self.nIndividual: int = n
        self.nTask: int = tasks.size()
        self.tasks: list[Task] = tasks

        max: int = 0
        min: int = sys.maxsize

        for task in self.tasks:
            if task.getLenGen() > max:
                max = task.getLenGen()
            if task.getLenGen() < min:
                min = task.getLenGen()
        self.lenGen = max

    def init(self):
        individuals: list = []

        for i in range(0, self.nIndividual, 1):
            g: list[float] = random.sample(range(0, 1), self.lenGen)

            if self.checkIndividualVail(g):
                self.makeIndividualVail(g)

            fitnessTa: list[float] = [task.computeFitness(g) for task in self.tasks]

            ind = Individual(g, fitnessTa)
            individuals.add(ind)

        self.updateRankPopulation()

    def checkIndividualVail(self, ind: list[float]) -> bool:
        for task in self.tasks:
            if task.checkIndividualVail(ind):
                return True
        return False

    def makeIndividualVail(self, g: List[float]):
        i: int = 0
        xd: int = 0
        while True:
            t: Task = self.tasks.get(i)
            if t.checkIndividualVail(self.ind):
                xd = 0
                t.makeIndividualVail(self.ind)
            else:
                xd += 1
            if xd >= self.tasks.size():
                break
            i = (i + 1) % self.tasks.size()

    def updateRankPopulation(self):
        rankInTask: list[Individual] = [[] for _ in range(0, self.nTask, 1)]

        for i_in in range(self.nIndividual):
            ind: Individual = self.individuals.get(i_in)
            for i in range(self.nTask):
                lstIndividualInTask: list[Individual] = rankInTask.get(i);
                check: bool = True
                for j in range(0, lstIndividualInTask.size(), 1):
                    if lstIndividualInTask.get(j).getFitnessTask().get(i) > ind.getFitnessTask().get(i):
                        lstIndividualInTask.add(j, ind)
                        check = False
                        break
                if check:
                    lstIndividualInTask.add(ind)
                rankInTask.set(i, lstIndividualInTask)

        for i in range(self.nIndividual1):
            ind: Individual = self.individuals.get(i)
            factorial_rank: list[int] = []
            min_rank: int = self.nIndividual + 2
            task_rank_min: int = -1
            for j in range(self.nTask):
                rankJ: int = rankInTask.get(j).indexOf(ind) + 1
                factorial_rank.add(rankJ)
                if (rankJ < min_rank):
                    min_rank = rankJ
                    task_rank_min = j

            ind.setFactorial_rank(factorial_rank)
            ind.setSkillFactor(task_rank_min)
            ind.setScalarFitness(1.0 / min_rank)
