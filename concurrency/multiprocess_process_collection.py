from math import ceil
from multiprocessing import Process, Queue, current_process
import numpy as np
import os
import random
from time import time

def worker(input, output):
    for func, args in iter(input.get, 'STOP'):
        result = calculate(func, args)
        output.put(result)

def calculate(func, args):
    result = func(*args)
    print(f'{current_process().name}: {func.__name__}({args}) returned {result}')
    return result

def get_num_primes(num):

    primes = np.zeros((num), dtype=np.int64)

    n = 0  # The current number of primes
    for i in range(2, num):
        # Is i prime?
        for j in primes[:n]:
            if not i%j:
                # No
                break
        else:
            # Yes
            primes[n] = i
            n += 1
        i += 1
    return n

def coro_func(index, value):
    num = 10000*value
    t0 = time()
    n = get_num_primes(num)
    t1 = time()
    print(f'Process {index} done in {t1-t0:.2f} s (found {n} primes in [0, {num}])')
    return n


def main():
    num_procs = 3
    num_samples = 20
#    random.seed(0)
#    values = [random.randint(2,8) for _ in range(16)]
#    values = [i for i in reversed(range(num_samples))]
    values = [1]*num_samples
    values[0] = 10
    values[2] = 10
    values[num_samples-1] = 10

    # Create queues
    task_queue = Queue()
    done_queue = Queue()

    tasks = [(coro_func, (i, v)) for i, v in enumerate(values)]

    t0 = time()

    # Submit tasks
    for task in tasks:
        task_queue.put(task)

    # Start worker processes
    for i in range(num_procs):
        Process(target=worker, args=(task_queue, done_queue)).start()

    # Get and print results
    print(f'Unordered results: {[done_queue.get() for i in range(len(tasks))]}')

    # Tell child processes to stop
    for i in range(num_procs):
        task_queue.put('STOP')

    t1 = time()
    print(f'Done in {t1-t0:.2f} s')

if __name__ == "__main__":
    main()
