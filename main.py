from GeneticAlgorithm import GeneticAlgorithm

# Define jobs, machines, operators
jobs2 = [
    {"job": "J1", "machine": "M1", "time": 20},
    {"job": "J2", "machine": "M2", "time": 15},
    {"job": "J3", "machine": "M1", "time": 10},
    {"job": "J4", "machine": "M2", "time": 70},
    {"job": "J5", "machine": "M3", "time": 35},
    {"job": "J6", "machine": "M1", "time": 35},           
]


# Create an instance of the GeneticAlgorithm class with jobs2 as our job order
evolutionAlgo = GeneticAlgorithm(jobs2, 50, 3, 0.5, 0.9)

# Run everything
evolutionAlgo.run()

