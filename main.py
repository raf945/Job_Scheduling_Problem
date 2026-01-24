from Genetic import Genetic

import csv

jobs = []

# Read csv
with open('output.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        row['time'] = int(row['time'])
        row['priority'] = int(row['priority'])
        jobs.append(row)

# Define jobs, machines, operators
jobs2 = [
    {"job": "J1", "machine": "M1", "time": 20, "priority": 3, "tool": 'T1'},        
    {"job": "J2", "machine": "M2", "time": 30, "priority": 3, "tool": 'T1'},        
    {"job": "J3", "machine": "M1", "time": 10, "priority": 2, "tool": 'T3'},
]


# Create an instance of the GeneticAlgorithm class with jobs2 as our job order
evolutionAlgo = Genetic(jobs, 1000, 10, 1, 0.9)

evolutionAlgo.run()

