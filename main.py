from functions import *

# Define jobs, machines, operators
jobs2 = [
    {"job": "J1", "machine": "M1", "time": 20},
    {"job": "J2", "machine": "M2", "time": 25},
    {"job": "J3", "machine": "M1", "time": 40},
    {"job": "J4", "machine": "M3", "time": 40},
    {"job": "J5", "machine": "M2", "time": 45},
    {"job": "J6", "machine": "M1", "time": 35},
]

machines = {"M1": 0, "M2": 0, "M3": 0}  # available from time 0
operators = {"O1": 0}           		# available from time 0

schedule = []

# First we will create the job schedule list and shuffle jobs into it

x = 0
jobPermutations = []
    
# Shuffle jobs n times
shuffle(jobs2, jobPermutations)

while x <= 20:
    print(f'Epoch: {x} Started ////////////////////////////////////////')
    
    # Get the two new unrepaired children and 2 parents from generation 1
    childAList, childBList, nextGeneration = crossover(jobPermutations)
    
    # Find and repair duplicates of childA
    childAJobValues = findDuplicates(childAList, jobs2)
    childBJobValues = findDuplicates(childBList, jobs2)
    
    # Assign job constraints to job values in childAList
    childAFixed = getJobProcess(childAJobValues, jobs2)
    childBFixed = getJobProcess(childBJobValues, jobs2)
    
    # Mutate Child B, call it mutatedChildB - reverse order mutation
    mutatedChildB = mutateReverseOrder(childBFixed)

    # Mutate Child A, call it mutatedChild - plus 1 mutation
    mutatedChildA = mutatePlusOne(childAFixed)
    
    # Get the job permutations of the evolved list
    jobPermutations = addToNextGeneration(childAFixed, childBFixed, mutatedChildA, mutatedChildB, nextGeneration)

    # Get the lowest run time of job permutation from the evolved list
    print(getLowestRunTime(jobPermutations))

    print(f'Epoch: {x} ended ////////////////////////////////////////')    
    x+=1
