from DataSetGenerator import DataSetGenerator as DSG
from Genetic import Genetic
from Greedy import Greedy
from RandomAlgo import RandomAlgo
import time

# Random
class Benchmark():
    def __init__(self):
        # store seeds and dataset size to loop through later
        self.seeds = [1, 2]
        #self.seeds = [1, 31, 76, 89, 102]

        #self.dataset_size = [10, 25, 50, 100, 200]
        self.dataset_size = [10]

        # Initialise list of results
        self.randomResults = []
        self.greedyResults = []
        self.geneticResults = []
        self.improvement = []
        # genetic statistics
        #self.genetic_makespan_mean = []
        #self.genetic_runtime = []

    def runRandom(self):
        
        for problem_size in self.dataset_size:
            for seed in self.seeds:
                jobs = []
                dataset = DSG(problem_size, seed)
                dataset.runDataSet()
                dataset.read(jobs)

                # Start random
                start_time = time.time()
                random_experiment = RandomAlgo(jobs, seed)
                random_experiment.run()
                random_makespan = random_experiment.getCompletionTime()
                random_runtime = time.time() - start_time

                # Record results
                self.randomResults.append({'problem size': problem_size, 'seed': seed, 'makespan': random_makespan, 
                                           'runtime' : round(random_runtime, 4)})

        return self.randomResults
    
    # Pretty print the random results
    def getRandomResults(self):
        for result in self.randomResults:
            print(result)

            
    def runGreedy(self):
        
        for problem_size in self.dataset_size:
            for seed in self.seeds:
                jobs = []
                dataset = DSG(problem_size, seed)
                dataset.runDataSet()
                dataset.read(jobs)

                # Start greedy algorithm
                start_time = time.time()
                greedy_experiment = Greedy(jobs)
                greedy_experiment.run()
                greedy_makespan = greedy_experiment.getCompletionTime()
                greedy_runtime = time.time() - start_time

                # Record results
                self.greedyResults.append({'problem size': problem_size, 'seed': seed, 'makespan': greedy_makespan, 
                                           'runtime' : round(greedy_runtime, 4)})

        return self.greedyResults
    

    # Pretty print the greedy results
    def getGreedyResults(self):
        for result in self.greedyResults:
            print(result)

    
    # Genetic Algorithm
    def runGeneticAlgorithm(self):
        for problem_size in self.dataset_size:
            print(problem_size)
            
            for seed in self.seeds:
                jobs = []
                dataset = DSG(problem_size, seed)
                dataset.runDataSet()
                dataset.read(jobs)

                genetic_makespan = []
                genetic_runtime = []

                for run in range(2):
                    # Start random algorithm
                    start_time = time.time()
                    genetic_experiment = Genetic(jobs, 15 , 3, 0.3, 0.7)
                    genetic_experiment.run()
                    genetic_makespan.append(genetic_experiment.getCompletionTime())
                    genetic_runtime.append(time.time() - start_time)

                # Record results
                self.geneticResults.append({'problem size': problem_size, 
                                            'seed': seed, 
                                            'makespan best': min(genetic_makespan),
                                            'makespan mean' : sum(genetic_makespan) / 2, 
                                            'runtime' : round(sum(genetic_runtime) / 2, 4)})
            
                
    # Pretty print the greedy results
    def getGeneticResults(self):
        for result in self.geneticResults:
            print(result)

    # Calculate improvement of GA over random and greedy algorithms
    def calculateImprovements(self):

        comparisonLength = len(self.geneticResults)

        for metric in range(comparisonLength):
            genetic_makespan_best = self.geneticResults[metric]['makespan best']
            greedy_makespan = self.greedyResults[metric]['makespan']
            random_makespan = self.randomResults[metric]['makespan']
            
            self.improvement.append({'problem size': self.geneticResults[metric]['problem size'],
                                'seed': self.geneticResults[metric]['seed'],
                                'Genetic Best makespan': genetic_makespan_best,
                                'Genetic Mean makespan': self.geneticResults[metric]['makespan mean'],
                                'Greedy makespan': greedy_makespan,
                                'Random makespan': random_makespan,
                                'Genetic improvement vs greedy %': round((greedy_makespan - genetic_makespan_best) / greedy_makespan * 100, 2),
                                'Genetic improvement vs random %': round((random_makespan - genetic_makespan_best) / random_makespan * 100, 2)
                            })
                        
        return self.improvement
    
    # Pretty print improvements
    def getImprovementResults(self):
        print('improvements')
        for result in self.improvement:
            print(result)
    

myBenchmark = Benchmark()
myBenchmark.runRandom()
myBenchmark.runGreedy()
myBenchmark.runGeneticAlgorithm()
print('')
print("Random Results")
print('')
myBenchmark.getRandomResults()
print('')
print("Greedy Results")
print('')
myBenchmark.getGreedyResults()
print('')
print("Genetic ALgorithm Results")
print('')
myBenchmark.getGeneticResults()
print('')
print('Improvements')
print('')
myBenchmark.calculateImprovements()
myBenchmark.getImprovementResults()