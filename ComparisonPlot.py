import matplotlib.pyplot as plt
import pandas as pd


class ComparisonPlot():
    def __init__(self):
        # Read CSV
        self.improvements = pd.read_csv('improvements.csv')
        self.benchmark = pd.read_csv('benchmark_output.csv')
        # Makespan for chart 1
        self.random_makespan = []
        self.greedy_makespan = []
        self.genetic_makespan = []
        self.problem_sizes = [10, 25, 50, 100, 200]

        # Improvements for chart 2
        self.improvement_greedy = []
        self.improvement_random = []

        # Runtimes for chart 3
        self.random_runtime = []
        self.greedy_runtime = []
        self.genetic_runtime = []

    # Create the makespan line chart
    def makespanComparison(self):

        # Get makespan
        for jobOrder in self.problem_sizes:
            self.random_makespan.append(self.benchmark[(self.benchmark['algorithm'] == 'random') & (self.benchmark['problem size'] == jobOrder)]['makespan'].mean())
            self.greedy_makespan.append(self.benchmark[(self.benchmark['algorithm'] == 'Greedy') & (self.benchmark['problem size'] == jobOrder)]['makespan'].mean())
            self.genetic_makespan.append(self.benchmark[(self.benchmark['algorithm'] == 'Genetic') & (self.benchmark['problem size'] == jobOrder)]['makespan'].mean())
        
        # Line graph showing the makespan as the number of jobs increase
        plt.figure(figsize=(10, 6))
        plt.plot(self.problem_sizes, self.random_makespan, label='Random', color='blue')
        plt.plot(self.problem_sizes, self.greedy_makespan, label='Greedy', color='black')
        plt.plot(self.problem_sizes, self.genetic_makespan, label='Genetic Algorithm', color='red')
        plt.xlabel('Number of jobs', fontsize=10)
        plt.ylabel('Makespan', fontsize=10)
        plt.title('Makespan Comparison', fontsize=14, fontweight='bold')
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3)
        plt.savefig('makespan_comparison.png', dpi=300)
        plt.show()

    # Create improvement comparison
    def improvementComparison(self):
        # Get mean of both improvements, genetic vs greedy and genetic vs random
        for size in self.problem_sizes:
            size_improvements = self.improvements[self.improvements['problem size'] == size]
            self.improvement_greedy.append(size_improvements['Genetic improvement vs greedy %'].mean())
            self.improvement_random.append(size_improvements['Genetic improvement vs random %'].mean())

        # Create bar chart
        plt.figure(figsize=(10, 6))
        x = range(len(self.problem_sizes))
        width = 0.35

        plt.bar([i - width/2 for i in x], self.improvement_greedy, width, label='Genetic vs Greedy', color='blue', alpha=0.8)
        plt.bar([i + width/2 for i in x], self.improvement_random, width, label='Genetic vs Random', color='red', alpha=0.8)

        plt.xlabel('Number of jobs', fontsize=10)
        plt.ylabel('Improvement', fontsize=10)
        plt.title('Genetic Algorithm Improvement Versus Baseline', fontsize=14, fontweight='bold')
        plt.xticks(x, self.problem_sizes)
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        plt.savefig('genetic_improvement.png', dpi=300,)
        plt.show()

    # Runtime comparison
    def runtimeComparison(self):
        # Get runtime mean
        for size in self.problem_sizes:
            self.random_runtime.append(self.benchmark[(self.benchmark['algorithm'] == 'random') & (self.benchmark['problem size'] == size)]['runtime'].mean())
            self.greedy_runtime.append(self.benchmark[(self.benchmark['algorithm'] == 'Greedy') & (self.benchmark['problem size'] == size)]['runtime'].mean())
            self.genetic_runtime.append(self.benchmark[(self.benchmark['algorithm'] == 'Genetic') & (self.benchmark['problem size'] == size)]['runtime'].mean())

        # create bar chart
        plt.figure(figsize=(10, 6))
        x = range(len(self.problem_sizes))
        width = 0.25

        plt.bar([i - width for i in x], self.random_runtime, width, label='Random', color='blue')
        plt.bar([i for i in x], self.greedy_runtime, width, label='Greedy', color='black')
        plt.bar([i + width for i in x], self.genetic_runtime, width, label='Genetic Algorithm', color='red')

        plt.xlabel('Number of Jobs', fontsize=12)
        plt.ylabel('Runtime seconds in log scale', fontsize=12)
        plt.title('Runtime Comparison', fontsize=14, fontweight='bold')
        plt.xticks(x, self.problem_sizes)
        plt.yscale('log')
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        plt.savefig('runtime_comparison.png', dpi=300, bbox_inches='tight')
        plt.show()
