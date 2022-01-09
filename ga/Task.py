class Task(object):
    def __init__(self, dimension: int, capacity: int):
        self.dimension: int = dimension
        self.capacity: int = capacity

    def getStride(self, tx: list[float], tmp_tx: list[float], window: list[float]) -> int:
        stride: int
        if (tmp_tx.size() - window.length) % (self.dimension - 1) == 0:
            stride = (tmp_tx.size() - window.length) / (self.dimension - 1)
        else:
            stride = (tmp_tx.size() - window.length) / (self.dimension - 1) + 1
            zero_padding: int = (self.dimension - 1) * stride + window.length - tx.size()
            for i in range(0, zero_padding, 1):
                tmp_tx.add(0.0)
        return stride

    def computeFitness(self, individual: list[float]) -> float:
        pass

    def makeIndividualVail(self, individual: list[float]):
        pass

    def checkIndividualVail(self, individual: list[float]) -> bool:
        pass

    def getLenGen(self):
        pass
