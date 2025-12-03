import random
import copy
import math
# TURN THIS ALL INTO A CLASS!!!! - TO DO!

# Define jobs, machines, operators
jobs = [
    {"job": "J1", "machine": "M1", "time": 20},
    {"job": "J2", "machine": "M2", "time": 25},
    {"job": "J3", "machine": "M3", "time": 40},
    {"job": "J4", "machine": "M2", "time": 40},
    {"job": "J5", "machine": "M3", "time": 45},
    {"job": "J6", "machine": "M2", "time": 65},
]

machines = {"M1": 0, "M2": 0, "M3": 0}  # available from time 0
operators = {"O1": 0}           		# available from time 0

schedule = []

# Function that copies jobs list and randomises them - Returns a list of lists that each have a randomised job order
def shuffle(list_param, jobPermutations):
    # Here we are adding the original job order to the jobPermutations list
    x = 0
    originalJobOrder = copy.deepcopy(list_param)
    jobPermutations.append(originalJobOrder)

    # while loop so that the original job order is shuffled until 
    while x < (len(list_param)-1):
        individual = copy.deepcopy(list_param)
        random.shuffle(individual)
        jobPermutations.append(individual)
        x+=1

# This will apply the schedule algorithm to one job permutation - Returns a run time of the list of job orders
def scheduleMachines(loop, jobPermutations):

    # Temp fix
    schedule.clear()


    machines = {"M1": 0, "M2": 0, "M3": 0}  # available from time 0
    operators = {"O1": 0} 

    for job in jobPermutations[loop]:
        #print(jobPermutations)
        machine = job["machine"]
        
        # Find the operator that is available the earliest
        available_operator = min(operators, key=lambda x: operators[x])
        
        # Determine start time (max of machine and operator availability)
        start_time = max(machines[machine], operators[available_operator])
        end_time = start_time + job["time"]
        
        # Update availability
        machines[machine] = end_time
        operators[available_operator] = operators[available_operator] + 10
        
        # Save schedule
        schedule.append({
            "job": job["job"],
            "machine": machine,
            "operator": available_operator,
            "start": start_time,
            "end": end_time
        })
        print(f"{job['job']} starts at {start_time}, ends at {end_time}, machine: {machine}, operator: {available_operator}")

    # Print schedule
    for s in schedule:
        print(f"Job {s['job']} -> Machine: {s['machine']}, Operator: {s['operator']}, "
            f"Start: {s['start']}, End: {s['end']}")

    # Total runtime
    total_runtime = max([s["end"] for s in schedule])
    print(f"\nTotal runtime: {total_runtime} minutes")

    schedule.clear()

    return total_runtime


# crossover function that creates a new generation from old
# Gets the two highest performers + crossover
def crossover(jobPermuations_param):

    # Create a generation of run times
    generation = []

    # Run the schedule algorithm on each job order and add to generation list
    for iteration in range(len(jobPermuations_param)):
        runtime = scheduleMachines(iteration, jobPermuations_param)
        generation.append((runtime, jobPermuations_param[iteration]))

    # sorts by runtime
    generation.sort(key=lambda x: x[0])

    # Get the two highest performers add to next generation
    nextGeneration = generation[:2]

    # Store one runtime + job order
    generation_firstParent = nextGeneration[0]
    generation_secondParent = nextGeneration[1]

    # Store ONLY job order
    generation_firstParent_JobOrder = generation_firstParent[1]
    generation_secondParent_JobOrder = generation_secondParent[1]

    # Add two parent job orders for evolution

    evolution = []

    evolution.append(generation_firstParent_JobOrder)
    evolution.append(generation_secondParent_JobOrder)
    
    # Define childA and childB, length of job order for crossover
    childA = []
    childB = []
    jobOrderHalved = (math.floor(len(generation_firstParent[1])/2))

    # Get first half of parent A and second half of parent B, breed child A
    childA.append(generation_firstParent_JobOrder[:jobOrderHalved])
    childA.append(generation_secondParent_JobOrder[jobOrderHalved:])

    # Combine the two lists inside child A into childAList
    childAList = childA[0] + childA[1]

    # Get first half of parent B and second half of parent A, breed child B
    childB.append(generation_secondParent_JobOrder[:jobOrderHalved])
    childB.append(generation_firstParent_JobOrder[jobOrderHalved:])

    # Combine the two lists inside child B into childBList
    childBList = childB[0] + childB[1]


    return childAList, childBList, evolution


# Here we are finding the duplicate jobs in the children then adding what is missing
def findDuplicates(childA, jobOrder):

    # This is a list which just gets all the job values and puts them into a list
    jobValues = [j['job'] for j in childA]

    # This is the default list of job values
    jobRegularList = [j['job'] for j in jobOrder]

    # Convert job values into dictionary to remove duplicates
    jobValuesNoDuplicates = list(dict.fromkeys(jobValues))

    # Get what is missing
    exampleSet = set(jobRegularList) - set(jobValuesNoDuplicates)

    # Add what is missing
    jobValuesNoDuplicates+= exampleSet

    return jobValuesNoDuplicates


# Getting the job contraints and machines back into a dictionary
def getJobProcess(childJobValues, basicJobOrder):
    # Create a lookup: job name -> full dict
    job_lookup = {job['job']: job for job in basicJobOrder}
    
    # This is loop that looks through a job dictionary and assigned the child job value to the job order
    result = []
    for job_name in childJobValues:
        if job_name in job_lookup:
            result.append(job_lookup[job_name])
        else:
            raise ValueError(f"Job {job_name} not found in basic job order!")
    
    return result

# Move every dictionary in child list to the right by +1
def mutatePlusOne(child):
    
    # temporary stores for last variable to go in front
    temp_lastJobStore = child[(len(child)-1)]

    #Mutated List
    mutatedChild = [temp_lastJobStore]

    x = 0 # Iteration count
    y = 1 # Second dictionary in list

    # Loop that adds
    while y <= (len(child)-1):
        mutatedChild.append(child[x])
        y+=1
        x+=1        
    #print(f'Mutated Child = {mutatedChild}')

    return mutatedChild


# Write a function that reverses the order of the job dictionaries
def mutateReverseOrder(listChild):
    
    reversed_copy = listChild[:]        # or listChild.copy()
    reversed_copy.reverse()                     # now safe to modify
    return reversed_copy


# Schedule machines on children
def addToNextGeneration(childA, childB, childC, childD, nextGen):

    # Create array that will hold next generation
    evolution = []

    # Add 2 best performers to next generation and 4 children
    evolution.append(nextGen[0])
    evolution.append(nextGen[1])
    evolution.append(childA)
    evolution.append(childB)
    evolution.append(childC)
    evolution.append(childD)
    
    return evolution

# This will take the list of list output from addToNextGeneration and get the lowest run time
def getLowestRunTime(evolution):

    # Define x as the loop iterator, runTimes initialised to hold the run time
    x = 0

    # Job order list will hold all the job order + run time dictionaries
    jobOrderList = []

    # While loop is used to loop because I find it easier
    while x < len(evolution):

        # Create a new dictionary everytime to assign job order and run time
        # We also schedule the machines here as we only need the run time of the job order
        jobOrderRunTimes = {"Job Order": evolution[x],
                            'RunTime': scheduleMachines(x, evolution)
                            }

        # Add job order + runtimes to dictionary, increment x by one til we reach the end of the list of list job orders
        jobOrderList.append(jobOrderRunTimes)
        x+=1

    # Sort the job order list of dictionaries by lowest to highest run time
    lowestToHighestRunTime = sorted(jobOrderList, key=lambda x: x["RunTime"])

    # Get the first index value of sorted job order list of dictionaries
    lowestRunTime = lowestToHighestRunTime[0]['RunTime']

    # Return single integer, lowest run time of evolution
    return lowestRunTime 

"""
# Random job list

randomJobList = []

# Create the job permutations n times
shuffle(jobs, randomJobList)

print(f'Random job list: {randomJobList}')

print(f'Length of job list {len(randomJobList)}')

#def geneticAlgorithm(iterations):

# Get the two new unrepaired children and 2 parents from generation 1
childAList, childBList, nextGeneration = crossover(randomJobList)

# Find and repair duplicates of childA
childAJobValues = findDuplicates(childAList, jobs)
childBJobValues = findDuplicates(childBList, jobs)

# Assign job constraints to job values in childAList
childAFixed = getJobProcess(childAJobValues, jobs)
childBFixed = getJobProcess(childBJobValues, jobs)

# Mutate Child B, call it mutatedChildB - reverse order mutation
mutatedChildB = mutateReverseOrder(childBFixed)

# Mutate Child A, call it mutatedChild - plus 1 mutation
mutatedChildA = mutatePlusOne(childAFixed)

print('##############')

# Get the job permutations of the evolved list
evolutionGen = addToNextGeneration(childAFixed, childBFixed, mutatedChildA, mutatedChildB, nextGeneration)

# Get the lowest run time of job permutation from the evolved list
print(getLowestRunTime(evolutionGen))

"""


