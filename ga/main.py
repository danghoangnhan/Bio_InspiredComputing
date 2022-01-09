from ga.MFEA import MFEA
from ga.Task import Task
from task.Knapsack import Knapsack
from task.TSP import TSP

tasks: list[Task] = [
    Knapsack("data/knapsack/100/s000.kp"),
    Knapsack("data/knapsack/100/s001.kp"),
    Knapsack("data/knapsack/100/s002.kp"),
    Knapsack("data/knapsack/100/s003.kp"),
    Knapsack("data/knapsack/100/s004.kp"),
    TSP("data/tsp/kroA100.tsp")
]

multitaskingAlgorithm = MFEA(tasks, 50, 0.1, 50)
multitaskingAlgorithm.run(50)
