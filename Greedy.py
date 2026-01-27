import csv
import copy

"""
jobs = []

# Read csv
with open('output.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        row['time'] = int(row['time'])
        row['priority'] = int(row['priority'])
        jobs.append(row)
"""

class Greedy():
    def __init__(self, dataset):
        self.dataset = dataset
        self.scheduledJobs =[]
        self.completionTime = 0


    def rank(self):
        # Sort by priority, then by time, then by machine
        self.dataset.sort(key=lambda x: (x["priority"], x["time"], x["machine"]))

    # Schedule code refactored and expanded upon from LAB 3 by Dr Deniz Cetinkaya
    def scheduleJobs(self):
        
        # Reset Assignment
        self.schedule =[]
        self.machines = {"M1": 0, "M2": 0, "M3": 0, "M4": 0, "M5": 0}
        self.operators = {"O1": 0, "O2": 0, "O3": 0}
        self.tools = {"T1": 0, "T2": 0, 'T3': 0}

        for job in self.dataset:

            machine = job["machine"]
            tool = job['tool']
            
            # Find the operator that is available the earliest
            available_operator = min(self.operators, key=lambda x: self.operators[x])
            
            # Determine start time (max of machine, operator and tool availability)
            start_time = max(self.machines[machine], self.operators[available_operator], self.tools[tool])
            end_time = start_time + job["time"]
            
            # Update availability
            self.machines[machine] = end_time
            self.operators[available_operator] = end_time
            self.tools[tool] = end_time

            # Save schedule
            self.schedule.append({
                "job": job["job"],
                "machine": machine,
                "operator": available_operator,
                "tool": tool,
                "start": start_time,
                "end": end_time,
                "priority": job["priority"]
            })
            print(f"{job['job']} starts at {start_time}, ends at {end_time}, machine: {machine}, operator: {available_operator}, using tool: {tool}")


        # Print schedule
        for s in self.schedule:
            print(f"Job {s['job']} -> Machine: {s['machine']}, Operator: {s['operator']}, Priority: {s['priority']},Tool: {s['tool']} "
                f"Start: {s['start']}, End: {s['end']}")

        # Total runtime
        total_runtime = max([s["end"] for s in self.schedule])
        print(f"\nTotal runtime: {total_runtime} minutes")

        self.scheduledJobs.append((total_runtime, self.dataset))
        self.completionTime = total_runtime

        return self.scheduledJobs
    
    
    def getCompletionTime(self):
        return self.completionTime
    
    
    def getJobOrders(self):
        return self.scheduledJobs
    
    def run(self):
        self.rank()
        self.scheduleJobs()
                
