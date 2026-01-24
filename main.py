from GeneticAlgorithm import GeneticAlgorithm
from Genetic import Genetic

# Define jobs, machines, operators
jobs2 = [
    {"job": "J1", "machine": "M1", "time": 20, "priority": 3, "tool": 'T1'},        
    {"job": "J2", "machine": "M2", "time": 30, "priority": 3, "tool": 'T1'},        
    {"job": "J3", "machine": "M1", "time": 10, "priority": 2, "tool": 'T3'},
]


# Create an instance of the GeneticAlgorithm class with jobs2 as our job order
evolutionAlgo = Genetic(jobs2, 4, 4, 1, 0.9)

evolutionAlgo.run()

