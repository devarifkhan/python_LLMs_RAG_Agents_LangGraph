from multiprocessing import Queue,Process

def worker(q):
    q.put('Hello from worker!')
    

if __name__ == '__main__':
    q = Queue()
    p = Process(target=worker, args=(q,))
    p.start()
    p.join()

    message = q.get()
    print(message)  # Output: Hello from worker!