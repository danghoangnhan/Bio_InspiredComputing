from abc import ABC
from typing import List

from ga.Task import Task


class Node:
    def __init__(self, index, x, y):
        self.index = index
        self.x = x
        self.y = y


class cvrp(Task, ABC):
    def __init__(self, fileName):
        self.parseFile(fileName)
        self.stride = 0

    def parseFile(self, fileName: str):
        with open(fileName) as file:
            lines = [line.rstrip() for line in file.readlines()]
            self.ProblemName = lines[0].replace("NAME : ", "")
            self.comment = lines[1].replace("COMMENT :", "")
            self.TYPE = lines[2].replace("TYPE : ", "")
            self.dimension = int(lines[3].replace("DIMENSION : ", ""))
            self.EDGE_WEIGHT_TYPE = lines[4].replace("EDGE_WEIGHT_TYPE : ", "")
            self.capacity = int(lines[5].replace("CAPACITY : ", ""))
            index = [int(x) for x in file.read().split()]
            self.NODE_COORD_SECTION = List[Node] = []
            self.DEMAND_SECTION = List[int] = []
            for i in range(self.dimension):
                self.NODE_COORD_SECTION.append()
