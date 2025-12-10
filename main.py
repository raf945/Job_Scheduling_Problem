from GeneticAlgorithm import GeneticAlgorithm

# Define jobs, machines, operators
jobs2 = [
    {"job": "J1", "machine": "M1", "time": 20},
    {"job": "J2", "machine": "M2", "time": 15},
    {"job": "J3", "machine": "M1", "time": 10},
    {"job": "J4", "machine": "M3", "time": 70},
    {"job": "J5", "machine": "M2", "time": 35},
    {"job": "J6", "machine": "M1", "time": 35},           
]


# Create an instance of the GeneticAlgorithm class with jobs2 as our job order
evolutionAlgo = GeneticAlgorithm(jobs2, 6, 3, 0.5, 0.9)

# Call the shuffle function to create a list of job lists each with a difference job order dictionary order
evolutionAlgo.shuffle()

# Schedule machines and return list of tuples. Each tuple has a run time and its corresponding job order
evolutionAlgo.scheduleMachines()

# Get the best two performers
evolutionAlgo.getParents()

# Apply the crossover function
x = 0
while x < 1:
    print(evolutionAlgo.crossover())
    x+=1