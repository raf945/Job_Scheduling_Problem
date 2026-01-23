from GeneticAlgorithm import GeneticAlgorithm
from Genetic import Genetic

# Define jobs, machines, operators
jobs2 = [
    {"job": "J1", "machine": "M1", "time": 20, "priority": 2, "tool": 'T1'},        
    {"job": "J2", "machine": "M2", "time": 30, "priority": 3, "tool": 'T1'},        
    {"job": "J3", "machine": "M1", "time": 10, "priority": 2, "tool": 'T3'},
    {"job": "J4", "machine": "M2", "time": 15, "priority": 1, "tool": 'T2'},
    {"job": "J5", "machine": "M1", "time": 40, "priority": 2, "tool": 'T3'},
    {"job": "J6", "machine": "M3", "time": 30, "priority": 1, "tool": 'T3'},
    {"job": "J7", "machine": "M1", "time": 15, "priority": 1, "tool": 'T2'},
    {"job": "J8", "machine": "M3", "time": 65, "priority": 2, "tool": 'T1'},
    {"job": "J9", "machine": "M3", "time": 45, "priority": 3, "tool": 'T3'},
    {"job": "J10", "machine": "M2", "time": 10, "priority": 3, "tool": 'T3'},
]


# Create an instance of the GeneticAlgorithm class with jobs2 as our job order
evolutionAlgo = Genetic(jobs2, 100, 5, 0.5, 0.9)

evolutionAlgo.run()

