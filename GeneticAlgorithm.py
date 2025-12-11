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
        self.nextGeneration = []

        # Parent A, parent B
        self.parentA = []
        self.parentB = []

        # Child A, child B
        self.childA = []
        self.childB = []

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

    # Getter function to get the original job permutations list
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
        self.firstGeneration.append((total_runtime, copy.deepcopy(self.jobPermutations[index])))


        # self.schedule.clear()

        return self.scheduleMachines(index + 1)
    
    # Write the function for sorting the job permutation tuple list by runtime and get the two best performers
    def getParents(self):

        # Sort all tuples in the list by the first element in the tuple which would be the runtime, therefore giving us the best performers
        self.firstGeneration.sort(key=lambda y: y[0], reverse=False)

        # Assigned parent A and B to the best performers in the first generation
        self.parentA = (self.firstGeneration[0])
        self.parentB = (self.firstGeneration[1])

    def printFirstGeneration(self):
        return self.parentA, self.parentB


    # Write the crossover function
    def crossover(self):
        x = random.random()

        # First we will apply the crossover rate so that way we dont always crossover two parents to avoid a local minima
        if x > self.crossover_rate:
            return 'Crossover not applied'

        # If x smaller than the crossover rate then we crossover the two parents
        # Here we assigned the parents' job order dicts from the two tuples
        parentAJobOrder = self.parentA[1]
        parentBJobOrder = self.parentB[1]

        # Get the length of job order for crossover
        jobOrderHalved = (math.floor(len(parentAJobOrder)/2))

        print(f'job order length = {jobOrderHalved}')

        # Get first half of parent A and second half of parent B for child A
        tempHoldingForChildA = []
        tempHoldingForChildA.append(parentAJobOrder[:jobOrderHalved])
        tempHoldingForChildA.append(parentBJobOrder[jobOrderHalved:])

        self.childA = tempHoldingForChildA[0] + tempHoldingForChildA[1]

        # Get first half of parent B and second half of parent A for child A
        tempHoldingForChildB = []
        tempHoldingForChildB.append(parentBJobOrder[:jobOrderHalved])
        tempHoldingForChildB.append(parentAJobOrder[jobOrderHalved:])

        self.childB = tempHoldingForChildB[0] + tempHoldingForChildB[1]

    # Finds duplicates in the job order and returns a list of strings with a unique jobs order
    def findDuplicates(self, child):

        # This is a list which just gets all the job values and puts them into a list
        jobValues = [j['job'] for j in child]

        # This is the default list of job values
        jobRegularList = [j['job'] for j in self.jobOrder]

        # Assign none to duplicates
        seen = set()
        for i, job in enumerate(jobValues):
            if job in seen:
                jobValues[i] = None
            else:
                seen.add(job)


        uniqueValues = jobValues.copy()

        print(f'uniqueValues: {uniqueValues}')

        # Get what is missing
        missing = [j for j in jobRegularList if j not in uniqueValues]
        print(f"Missing jobs: {missing}")

        # Add what is missing
        x=0
        for index, job in enumerate(uniqueValues):
            if job == None:
                uniqueValues[index] = missing[x]
                x+=1

        print(f'This should be a fixed list: {uniqueValues}')
        # Create a lookup: job name -> full dict

        job_lookup = {job['job']: job for job in self.jobOrder}
        
        # This is loop that looks through a job dictionary and assigned the child job value to the job order
        result = []
        for job_name in uniqueValues:
            if job_name in job_lookup:
                result.append(job_lookup[job_name])
            else:
                raise ValueError(f"Job {job_name} not found in basic job order!")

        print(f'Final result of Child A: {result}')

        child = result


    def getChildren(self):
        print(f'childA:{self.childA}')
        print('\n')
        print(f'childB:{self.childB}')

    # Write the select two random jobs function - Write this after the repair function
    def twoRandomJobs(self):

        # Assign child list we want to mutate and create two random numbers that are not the same
        holdingList = copy.deepcopy(self.childA)
        jobOne = random.randrange(0,5)
        jobTwo = random.randrange(0,5)

        while jobOne == jobTwo:
            jobTwo = random.randrange(0,5)
            print('loop')

        print( f'Child A DNA{self.childA}')
        print( f'Copy of Child A DNA{holdingList}')
        

    # Right now findDuplicates, only repairs childA, repair childB and any other
    # Write the fill the pop size algorithm

    # Write the mutatePlusOne function

    # Write the reverseMutate function

    def run(self):
        # Call the shuffle function to create a list of job lists each with a difference job order dictionary order
        self.shuffle()

        # Schedule machines and return list of tuples. Each tuple has a run time and its corresponding job order
        self.scheduleMachines()

        # Get the best two performers
        self.getParents()

        # Apply the crossover function
        self.crossover()

        self.getChildren()
        print('\n')

        # Repair DNA
        self.findDuplicates(self.childA)
        print('\n')

        self.findDuplicates(self.childB)
        # TODO  check if child A and Child B were repaired

