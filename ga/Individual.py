class Individual:
    def __init__(self, genome, fitnessTask, skillFactor: int = 0, scalarFitness: float = 0.0):
        self.scalarFitness = scalarFitness
        self.skillFactor: int = skillFactor
        self.gen: list[float] = genome
        self.fitnessTask: list[float] = fitnessTask
        self.factorial_rank: list = []

    def getMinFactorialRank(self) -> int:
        minInitial: int = 10000000
        minValue: int = min(self.fitnessTask)
        return minValue if minValue < minInitial else minInitial
