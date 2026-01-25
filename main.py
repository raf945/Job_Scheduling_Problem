from Genetic import Genetic
from Greedy import Greedy
from DataSetGenerator import DataSetGenerator as DSG
import csv

jobs = []

dataset = DSG(5, 3)
dataset.runDataSet()
# Read csv
with open('output.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        row['time'] = int(row['time'])
        row['priority'] = int(row['priority'])
        jobs.append(row)

# Create an instance of the GeneticAlgorithm class with jobs2 as our job order
evolutionAlgo = Genetic(jobs, 10, 5, 0.5, 0.5)
evolutionAlgo.run()

# Create an instance of the greedy algorithm as baseline
test = Greedy(jobs)
test.run()
print(f'Greedy Baseline: {test.getCompletionTime()}')
print(f'Genetic Algorithm: {evolutionAlgo.getCompletionTime()}')
print('')
print(f'Greedy job order: {test.getJobOrders()}')
print('')
print(f'Best Job order of Genetic Algorithm: {evolutionAlgo.mostOptimisedOrder()}')

