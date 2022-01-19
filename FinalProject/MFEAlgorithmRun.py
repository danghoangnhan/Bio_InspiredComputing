from ga.MFEA import MFEA
from task.Knapsack import Knapsack
from task.cvrp import cvrp
Tasks: list = [
    cvrp("data/com_vrp/instances/A/A-n32-k5.vrp")
]
g: MFEA = MFEA(Tasks, 50, 0.1, 50,ITERATION=10)
g.run(50,)
