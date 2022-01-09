from collections import namedtuple
from random import choices, randint
from typing import List, Callable

Genome = List[int]
Population = List[Genome]
FitnessFunc = Callable[[Genome], int]
Thing = namedtuple('Thing', ['name', 'value', 'weight'])

things = [
    Thing('Laptop', 500, 2200),
    Thing('Headphones', 150, 160),
    Thing('Coffee Mug', 60, 350),
    Thing('NotePad', 40, 333),
    Thing('Water Bottle', 500, 2200),
]


def generate_genome(length: int) -> Genome:
    return choices([0, 1], k=length)


def generate_population(size: int, genome_length: int) -> Population:
    return [generate_genome(genome_length) for _ in range(size)]


def fitness(genome: Genome, things: [Thing], weight_limit: int) -> int:
    if len(genome) != len(things):
        raise ValueError("genome and things must be off the same length")
    weight = 0
    value = 0

    for i, thing in enumerate(things):
        if (genome[i]) == 1:
            weight += thing.weight
            value += thing.value

            if weight > weight_limit:
                return 0

        return value


def selection_pair(population: Population, fitness_function: FitnessFunc) -> Population:
    return choices(
        population=population,
        weights=[fitness_function(genome) for genome in population],
        k=2
    )


def single_point_crossover(a: Genome, b: Genome) -> Tuple[Genome, Genome]:
    if len(a) != len(b):
        raise ValueError('Genomes a and b must be of same length')
    length = len(a)
    if length < 2:
        return a, b
    p = randint(1, length - 1)
    return a[0:p] + b[p:], b[0:p] + a[p:]

def mutation(genome:Genome,num:int=1,propability:float=0.5)->Genome:
    for _ in  range (num):
        index = randrange(len(genome))
        genome[index] = genome[index] if random() > propability else abs(genome[index])
    return genome
