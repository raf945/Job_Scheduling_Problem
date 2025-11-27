import random
import copy
import math

# Define jobs, machines, operators
jobs = [
    {"job": "J1", "machine": "M1", "time": 20},
    {"job": "J2", "machine": "M2", "time": 25},
    {"job": "J3", "machine": "M3", "time": 40},
    {"job": "J4", "machine": "M1", "time": 40},
    {"job": "J5", "machine": "M3", "time": 45},
    {"job": "J6", "machine": "M1", "time": 65},
]

machines = {"M1": 0, "M2": 20, "M3": 0}  # available from time 0
operators = {"O1": 0}           		# available from time 0

schedule = []

# Shuffle jobs list and add to list

jobPermutations = []

def shuffle(list_param):
    x = 0
    while x < len(list_param):
        individual = copy.deepcopy(jobs)
        random.shuffle(individual)
        jobPermutations.append(individual)
        x+=1

# This will apply the schedule algorithm to one job permutation
def scheduleMachines(loop):

    machines = {"M1": 0, "M2": 0, "M3": 0}  # available from time 0
    operators = {"O1": 0} 

    for job in jobPermutations[loop]:
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
        runtime = scheduleMachines(iteration)
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


    return childAList, childBList, nextGeneration


# Here we are finding the duplicate jobs in the children then adding what is missing
def findDuplicates(childA):

    # This is a list which just gets all the job values and puts them into a list
    jobValues = [j['job'] for j in childA]

    # This is the default list of job values
    jobRegularList = [j['job'] for j in jobs]

    # Convert job values into dictionary to remove duplicates
    jobValuesNoDuplicates = list(dict.fromkeys(jobValues))

    # Get what is missing
    exampleSet = set(jobRegularList) - set(jobValuesNoDuplicates)

    # Add what is missing
    jobValuesNoDuplicates+= exampleSet

    return jobValuesNoDuplicates


# Getting the job contraints and machines back into a dictionary
def getJobProcess(jobValues):

    # Create list that will hold our job dictionaries 
    childARepairedList = []

    # y is the comparison job variable, so if it is the same as x,
    # then we get the job dictionary with the value x and append it to childARepairedList
    y = 0
    z = 0

    # Loop that will assign job variables to job values
    for x in jobs:
        print(z)
        
        # If y becomes biger than the length of job values we set it to 0 and make another run through the job dictionaries
        if y > len(jobValues):
            y = 0

        # If the length of childARepairedList is bigger or equal to job values length, then that means we are done
        elif len(childARepairedList) >= len(jobValues):
            return childARepairedList

        # If the job value in child job Values matches the job value in the job dictionary
        # then we add that child job dictionary to our childARepairList
        elif x['job'] == jobValues[y]:

            childARepairedList.append(x)
            y += 1
        print(childARepairedList)

        z += 1


# Create the job permutations n times
shuffle(jobs)

# Get the two new unrepaired children and 2 parents from generation 1
childAList, childBList, nextGeneration = crossover(jobPermutations)

# Find and repair duplicates of childA
childAJobValues = findDuplicates(childAList)

print(childAJobValues)

# Assign job constraints to job values in childAList
print(getJobProcess(childAJobValues))


#print(jobs)



