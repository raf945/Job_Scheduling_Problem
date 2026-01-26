from Genetic import Genetic
from Greedy import Greedy
from RandomAlgo import RandomAlgo
from DataSetGenerator import DataSetGenerator as DSG
import csv

jobs = []

dataset = DSG(100, 1)
dataset.runDataSet()
dataset.read(jobs)
# Create an instance of the GeneticAlgorithm class with jobs2 as our job order
evolutionAlgo = Genetic(jobs, 100, 5, 0.7, 0.2)
#evolutionAlgo.run()

# Create an instance of the greedy algorithm as baseline
test = Greedy(jobs)
#test.run()

print('')
#print(f'Greedy job order: {test.getJobOrders()}')
print('')
#print(f'Best Job order of Genetic Algorithm: {evolutionAlgo.mostOptimisedOrder()}')

experiment_3 = RandomAlgo(jobs, 5)

experiment_3.run()

#print(f'Greedy Baseline: {test.getCompletionTime()}')
#print(f'Genetic Algorithm: {evolutionAlgo.getCompletionTime()}')
print(experiment_3.getCompletionTime())
