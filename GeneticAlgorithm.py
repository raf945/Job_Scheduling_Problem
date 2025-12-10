import random
import copy
import math

class GeneticAlgorithm:
    def __init__(self, jobOrder, pop_size, epoch, mutation_rate, crossover_rate):

        # Get the job order, pop_size we want and how many generations
        self.jobOrder = jobOrder
        self.pop_size = pop_size
        self.epoch = epoch

        # Set the mutation_rate and crossover_rate to avoid a local minima
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate

        # Initialise the job permutation list + firstGeneration
        self.jobPermutations = []
        self.firstGeneration =[]

        # Define the job contraints
        self.schedule = []
        self.machines = {"M1": 0, "M2": 0, "M3": 0}  # available from time 0
        self.operators = {"O1": 0}           		# available from time 0

    # Function that copies jobs list and randomises them - Returns a list of lists that each have a randomised job order
    def shuffle(self):

        # Here we are adding the original job order to the jobPermutations list
        x = 0
        originalJobOrder = copy.deepcopy(self.jobOrder)
        self.jobPermutations.append(originalJobOrder)

        # while loop so that the original job order is shuffled until 
        while x < self.pop_size-1:
            individual = copy.deepcopy(self.jobOrder)
            random.shuffle(individual)
            self.jobPermutations.append(individual)
            x+=1

    def getJobPerm(self):
        return f"size of the following list: {self.jobPermutations} is {len(self.jobPermutations)}"

    
    # This will apply the schedule algorithm to one job permutation - Returns a run time of the list of job orders

    def scheduleMachines(self, index=0):

        if index == self.pop_size:
            return self.firstGeneration

        # Temp fix
        self.schedule.clear()

        self.machines = {"M1": 0, "M2": 0, "M3": 0}  # available from time 0
        self.operators = {"O1": 0}

        for job in self.jobPermutations[index]:

            machine = job["machine"]
            
            # Find the operator that is available the earliest
            available_operator = min(self.operators, key=lambda x: self.operators[x])
            
            # Determine start time (max of machine and operator availability)
            start_time = max(self.machines[machine], self.operators[available_operator])
            end_time = start_time + job["time"]
            
            # Update availability
            self.machines[machine] = end_time
            self.operators[available_operator] = self.operators[available_operator] + 10
            
            # Save schedule
            self.schedule.append({
                "job": job["job"],
                "machine": machine,
                "operator": available_operator,
                "start": start_time,
                "end": end_time
            })
            print(f"{job['job']} starts at {start_time}, ends at {end_time}, machine: {machine}, operator: {available_operator}")


        # Print schedule
        for s in self.schedule:
            print(f"Job {s['job']} -> Machine: {s['machine']}, Operator: {s['operator']}, "
                f"Start: {s['start']}, End: {s['end']}")

        # Total runtime
        total_runtime = max([s["end"] for s in self.schedule])
        print(f"\nTotal runtime: {total_runtime} minutes")

        # Save total_runtime and job order to firstGeneration
        self.firstGeneration.append((total_runtime, self.jobPermutations[index]))

        # self.schedule.clear()

        return self.scheduleMachines(index + 1)
    
    # Write the function for sorting the job permutation tuple list by runtime and get the two best performers

    # Write the crossover function

    # Write the mutatePlusOne function

    # Write the reverseMutate function
