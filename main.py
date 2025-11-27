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
    print(f'last job = {temp_lastJobStore}')

    #Mutated List
    mutatedChild = [temp_lastJobStore]

    x = 0 # Iteration count
    y = 1 # Second dictionary in list

    # Loop that adds
    while y <= (len(child)-1):
        mutatedChild.append(child[x])
        y+=1
        x+=1        
    print(f'Mutated Child = {mutatedChild}')


# Create the job permutations n times
shuffle(jobs)

# Get the two new unrepaired children and 2 parents from generation 1
childAList, childBList, nextGeneration = crossover(jobPermutations)

# Find and repair duplicates of childA
childAJobValues = findDuplicates(childAList)
childBJobValues = findDuplicates(childBList)

# Assign job constraints to job values in childAList
childAFixed = getJobProcess(childAJobValues, jobs)
childBFixed = getJobProcess(childBJobValues, jobs)

print(childAFixed)

mutatePlusOne(childAFixed)




