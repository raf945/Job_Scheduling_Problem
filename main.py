import random
import copy

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
operators = {"O1": 0, "O2": 0}           		# available from time 0

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
    operators = {"O1": 0, "O2": 0} 

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
# Gets the two highest performers + crossover + mutate to create 4 more children
def crossover(jobPermuations_param):
    # Get the two highest performers add to next generation
    # Create a generation of run times
    generation = []

    for iteration in range(len(jobPermuations_param)):
        runtime = scheduleMachines(iteration)
        generation.append((runtime, jobPermuations_param[iteration]))

    generation.sort(key=lambda x: x[0])  # sorts by runtime

    return generation


print(crossover(jobPermutations))
print(len(jobs))




