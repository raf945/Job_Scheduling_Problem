import csv
import argparse
import os
from math import floor
import random
#import numpy as np

random.seed(1)

class DataSetGenerator():

    def __init__(self, jobsNumber, seed):
        self.jobsNumber = jobsNumber
        random.seed(seed)
        self.jobCounter = 0

        self.machineRandom = ""
        self.timeRandom = 0
        self.priority = 0
        self.toolRandom = ""
        self.machine_count = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0 }
        self.machine_weights=(20, 20, 20, 20, 20)

    def generateMachines(self):
        z = random.random()
        # For every 5 jobs,we assign
        if z < 0.6:
            # Round-robin assignment
            machine_number = (self.jobCounter % 5) + 1
            self.machineRandom = [machine_number]
            
        # First 5 jobs, assign randomly
        else:
            possible_machines = [1, 2, 3, 4, 5]
            self.machineRandom = random.choices(possible_machines, k=1)


    def generateConstraints(self):
        # Time
        self.timeRandom = max(5, floor(random.normalvariate(mu=30, sigma=15)))

        # Priority
        possible_priority = [1, 2, 3]
        self.priority = random.choices(possible_priority, weights=(10, 9, 9), k=1)

        # Tools
        t = random.random()
        if t < 0.8:
            tool_number = (self.jobCounter % 3) +1
            self.toolRandom = [tool_number]
        else:
            possible_tools = [1, 2, 3]
            self.toolRandom = random.choices(possible_tools, k=1)

    # Generate each job dictionary
    def generateDicts(self):
        self.jobCounter+=1
        
        jobDict = {"job": 'J'+ str(self.jobCounter), "machine": 'M'+ str(self.machineRandom[0]), 
                   "time": self.timeRandom, "priority": self.priority[0],
                   "tool": 'T'+ str(self.toolRandom[0])
                   }      
        return jobDict
    
    def runDataSet(self):
        self.jobPermutations = []

        while self.jobCounter < self.jobsNumber:
            self.generateMachines()
            self.generateConstraints()
            self.jobPermutations.append(self.generateDicts())

        with open('output.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['job', 'machine', 'time', 'priority', 'tool'])

            writer.writeheader()

            for jobRow in self.jobPermutations:
                writer.writerow(jobRow)

    def read(self, dataset):
        # Read csv
        with open('output.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row['time'] = int(row['time'])
                row['priority'] = int(row['priority'])
                dataset.append(row)

            return dataset

    def validate(self):
        print(f"Generated {len(self.jobPermutations)} jobs")
        print(f"processing time: {sum(j['time'] for j in self.jobPermutations) / len(self.jobPermutations)}")



