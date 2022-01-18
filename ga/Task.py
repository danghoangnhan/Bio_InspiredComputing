from abc import abstractmethod, ABCMeta


class Task:
    __metaclass__ = ABCMeta

    @abstractmethod
    def getStride(self, tx, tmp_tx, windowT):
        pass

    @abstractmethod
    def computeFitness(self, individual):
        pass

    @abstractmethod
    def makeIndividualVail(self, individual):
        pass

    @abstractmethod
    def checkIndividualVail(self, individual):
        pass

    @abstractmethod
    def getLenGen(self):
        pass

    @abstractmethod
    def parseFile(self, fileName):
        pass
