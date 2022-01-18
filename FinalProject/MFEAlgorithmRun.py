from ga.MFEA import MFEA
from task.Knapsack import Knapsack
Tasks: list = [
    Knapsack("data/knapsack/100/s000.kp"),
    Knapsack("data/knapsack/100/s001.kp")
]
g: MFEA = MFEA(Tasks, 50, 0.1, 50,ITERATION=10)
g.run(50,)
