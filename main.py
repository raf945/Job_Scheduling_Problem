from Benchmark import Benchmark
from BenchmarkToy import BenchmarkToy 
from ComparisonPlot import ComparisonPlot

# This is the real benchmark with all problem sizes and seeds. Will take about 45-60 minutes
"""
runProgram = Benchmark()
runProgram.runBenchmark()

improvementGraph = ComparisonPlot()
improvementGraph.improvementComparison()
improvementGraph.makespanComparison()
improvementGraph.runtimeComparison()
"""
# A benchmark with a toy dataset generator values to demonstrate that the code works

runProgram = BenchmarkToy()
runProgram.runBenchmark()

# Make sure to pip install matplotlib
improvementGraph = ComparisonPlot()
improvementGraph.improvementComparison()
improvementGraph.makespanComparison()
improvementGraph.runtimeComparison()



