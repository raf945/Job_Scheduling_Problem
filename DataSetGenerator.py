import csv
import argparse
import os
from math import floor, ceil
import random
#import numpy as np

random.seed(1)

class DataSetGenerator():

    def __init__(self, jobsNumber):
        self.jobsNumber = jobsNumber
        
        self.jobCounter = 0

        self.machineRandom = ""
        self.timeRandom = 0
        self.priority = 0
        self.toolRandom = ""
    
    def generateConstraints(self):
        # Machines
        possible_machines = [1, 2, 3, 4, 5]
        self.machineRandom = random.sample(possible_machines, 1)
        # Time
        self.timeRandom = random.randrange(5, 50, 5)

        # Priority
        """
        z = random.random() # Return float between 0.0 and 1.0
        if z > 0.5:
            self.priority = ceil(random.uniform(1, 5))
        else:
            self.priority = floor(random.uniform(1, 5))
        """
        possible_priority = [1, 2, 3, 4, 5]
        self.priority = random.choices(possible_priority, weights=(10, 8, 6, 4, 2), k=1)

        # Tools
        possible_tools = [1, 2, 3]
        self.toolRandom = random.choices(possible_tools, k=1)

        print(self.machineRandom)
        print(f'time: {self.timeRandom}')
        print(f'priority: {self.priority}')
        print(f'tools: {self.toolRandom}')

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
            self.generateConstraints()
            self.jobPermutations.append(self.generateDicts())
            #self.jobsNumber+1

        return self.jobPermutations      

example = DataSetGenerator(5)

example.runDataSet()

for x in example.jobPermutations:
    print(x)
    
