# CNC Job Scheduling with Genetic Algorithm

This project tackles a **Flexible Job Shop Scheduling Problem (FJSP)** for a CNC workshop.  
It schedules jobs across machines, operators and tools while respecting priorities, with the goal of minimising **makespan** (total completion time).

It demonstrates:

- Practical application of **metaheuristics (Genetic Algorithms)** to an **NP‑hard** optimisation problem
- End‑to‑end pipeline: **data generation → algorithms → benchmarking → visualisation**
- Strong Python skills (OOP, simulation, numerical work, plotting)

---

## Table of Contents
- [Problem Definition](#problem-definition)
- [What the Codebase Contains](#what-the-codebase-contains)
- [Algorithms For a Near Optimal Solution](#algorithms-for-a-near-optimal-solution)
  - [Random Baseline](#random-baseline)
  - [Greedy Heuristic](#greedy-heuristic)
  - [Genetic Algorithm (GA)](#genetic-algorithm-ga)
- [Benchmarking & Results](#benchmarking--results)
- [Visual Output (for Portfolio / GitHub)](#visual-output-for-portfolio--github)
  - [Makespan vs Number of Jobs](#makespan-vs-number-of-jobs)
  - [Genetic Algorithm – Improvement vs Baselines](#genetic-algorithm--improvement-vs-baselines)
  - [Runtime vs Number of Jobs (log scale)](#runtime-vs-number-of-jobs-log-scale)
  - [How to run](#how-to-run)
    - [Example script](#example-script)

## Problem Definition

A set of CNC jobs must be assigned to:

- **5 machines** – each can run **one job at a time**
- **3 operators** – each can supervise **one machine at a time**
- **3 tools** – each tool type has **only one copy**
- **Job priorities (1–3)** – higher‑priority work should complete earlier

The objective is to find a schedule that:

- Respects all resource and priority constraints
- Minimises the time when the **last job finishes** (makespan)

---

## What the Codebase Contains

**Core components**

- `DataSetGenerator.py` – creates realistic CNC job datasets and writes `output.csv`
- `RandomAlgo.py` – simple random‑plus‑priority baseline
- `Greedy.py` – deterministic heuristic (priority → processing time → machine)
- `Genetic.py` – full Genetic Algorithm optimiser
- `ComparisonPlot.py` – reads benchmark CSVs and outputs comparison charts
- `benchmark_output.csv` / `improvements.csv` – captured results for all runs

Technologies: **Python**, **pandas**, **matplotlib**, object‑oriented design.

---

## Algorithms For a Near Optimal Solution

All three schedulers share the same **discrete‑event simulation**:

- Track availability of each **machine**, **operator** and **tool**
- For each job, compute:
  - `start_time = max(machine_available, operator_available, tool_available)`
  - `end_time = start_time + processing_time`

The difference is **how the jobs are ordered**:

### Random Baseline

- Shuffles jobs randomly, then sorts by **priority**
- Very fast, but no notion of optimisation beyond priorities

### Greedy Heuristic

- Sorts jobs by:
  1. Priority (1 highest)
  2. Shortest processing time
  3. Machine ID
- Produces reasonable schedules in **milliseconds**

### Genetic Algorithm (GA)

- Chromosome = a permutation of jobs
- **Population:** 100 individuals  
- **Generations:** 50  
- **Operators:**
  - Tournament selection (sample 10, keep the best)
  - Single‑point crossover with repair to fix duplicates
  - Swap mutation with relatively high rate (0.3) to avoid local minima
- Evaluates each chromosome via the same resource‑constrained simulator
- Tracks the **best schedule and makespan** over all generations

---

## Benchmarking & Results

Benchmarks were run on problem sizes **10, 25, 50, 100, 200** jobs, using multiple random seeds.  
For each run, the code records:

- **Algorithm** (`random`, `Greedy`, `Genetic`)
- **Problem size**
- **Seed**
- **Makespan**
- **Runtime (seconds)**
- For GA: mean and worst makespan over generations
- Percentage improvement of GA vs Random and Greedy

**Key outcomes**

- For very small problems (10 jobs), all methods are similar – priorities dominate.
- As job count grows, the **Genetic Algorithm consistently achieves lower makespans**:
  - At 200 jobs, GA is about **13–14% better** than Greedy on total completion time.
  - On medium‑sized problems (25–50 jobs), GA often improves makespan by **20–25%** vs baselines.
- **Trade‑off:** - Random and Greedy finish in **milliseconds**.  
  - GA takes **seconds to minutes**, but delivers **significantly better schedules** – appropriate for offline planning or high‑value production runs.

---

## Visual Output (for Portfolio / GitHub)

The `ComparisonPlot` class produces three charts for the README or portfolio.

### Makespan vs Number of Jobs


![](https://github.com/raf945/Job_Scheduling_Problem/blob/main/makespan_comparison.png)

### Genetic Algorithm – Improvement vs Baselines

![](https://github.com/raf945/Job_Scheduling_Problem/blob/main/genetic_improvement.png)

### Runtime vs Number of Jobs (log scale)

![](https://github.com/raf945/Job_Scheduling_Problem/blob/main/runtime_comparison.png)

### How to run
```
pip install pandas matplotlib
```
#### Example script

```
from DataSetGenerator import DataSetGenerator
from RandomAlgo import RandomAlgo
from Greedy import Greedy
from Genetic import Genetic

# 1. Generate dataset
jobs = []
gen = DataSetGenerator(jobsNumber=50, seed=1)
gen.runDataSet()
gen.read(jobs)

# 2. Baselines
random_algo = RandomAlgo(dataset=jobs, seed=1)
random_algo.run()

greedy = Greedy(dataset=jobs.copy())
greedy.run()

# 3. Genetic Algorithm
ga = Genetic(jobOrder=jobs.copy(), pop_size=100, epoch=50,
             mutation_rate=0.3, crossover_rate=0.7)
ga.run()

print("Random:", random_algo.getCompletionTime())
print("Greedy:", greedy.getCompletionTime())
print("Genetic:", ga.getCompletionTime())
```


