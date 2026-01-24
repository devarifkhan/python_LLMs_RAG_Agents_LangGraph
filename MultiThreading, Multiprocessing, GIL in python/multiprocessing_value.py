def increment(counter):
from multiprocessing import Process, Value
import time

def simulate_visits(counter, n):
    for _ in range(n):
        time.sleep(0.001)
        with counter.get_lock():
            counter.value += 1

if __name__ == "__main__":
    total_visits = 5000
    num_processes = 5
    visits_per_process = total_visits // num_processes
    counter = Value('i', 0)

    processes = [Process(target=simulate_visits, args=(counter, visits_per_process)) for _ in range(num_processes)]
    for p in processes:
        p.start()
    for p in processes:
        p.join()

    print(f"Total simulated web page visits: {counter.value}")
