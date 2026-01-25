from multiprocessing import Queue, Process
import time

def worker(q, number):
    print(f"Worker processing: {number}")
    time.sleep(1)
    result = number * number
    q.put((number, result))

if __name__ == '__main__':
    numbers = [2, 4, 6, 8, 10]
    q = Queue()
    processes = []
    for n in numbers:
        p = Process(target=worker, args=(q, n))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    results = []
    while not q.empty():
        results.append(q.get())

    for number, squared in sorted(results):
        print(f"{number} squared is {squared}")