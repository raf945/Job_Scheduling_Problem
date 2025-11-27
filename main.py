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


# Create the job permutations n times
shuffle(jobs)

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


    return childAList, childBList


list1, list2 = crossover(jobPermutations)
print(list1)

print('')

# Here we are finding the duplicate jobs in the children
def findDuplicates(childA):

    # This is a list which just gets all the job values and puts them into a list
    jobNumber = [j['job'] for j in childA]
    # This is a list which will store what needs replacing and what doesnt

    # This is a loop which will compare all the values together and find duplicates
    for job in jobNumber:
        if job
    return jobNumber

print(findDuplicates(list1))


