from multiprocessing import Process
import time

def task(name):
    print(f"Task {name} starting")
    time.sleep(2)
    print(f"Task {name} completed")


start_time = time.time()


p1 = Process(target=task, args=("Task 1",))
p2 = Process(target=task, args=("Task 2",))


p1.start()
p2.start()

p1.join()
p2.join()

end_time = time.time()
print(f"Total time taken: {end_time - start_time} seconds")