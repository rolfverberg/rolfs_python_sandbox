from multiprocessing import Queue, Process, cpu_count
import numpy as np
import os
import random
from time import time

class UptownFunc:
    def __init__(self):
        pass

    def _func_queue(self, func, q_in, q_out, *args, **kwargs):
        """ Retrive processes from the queue """
        while True:
            pos, var = q_in.get()
            if pos is None:
                break

            res = func(var, *args, **kwargs)
            q_out.put((pos, res))
        return

    def parallelise_function(self, var, func, nprocs, *args, **kwargs):
        """ Split evaluations of func across processors """
        n = len(var)

        processes = []
        q_in = Queue(1)
        q_out = Queue()

        for i in range(nprocs):
            pass_args = [func, q_in, q_out]
            # pass_args.extend(args)

            p = Process(target=self._func_queue,\
                        args=tuple(pass_args),\
                        kwargs=kwargs)

            processes.append(p)

        for p in processes:
            p.daemon = True
            p.start()

        # put items in the queue
        sent = [q_in.put((i, var[i])) for i in range(n)]
        [q_in.put((None, None)) for _ in range(nprocs)]

        # get the results
        results = [[] for i in range(n)]
        for i in range(len(sent)):
            index, res = q_out.get()
            results[index] = res

        # wait until each processor has finished
        [p.join() for p in processes]

        # reorder results
        return results

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

def coro_func(value):
    num = 10000*value
    t0 = time()
    n = get_num_primes(num)
    t1 = time()
    print(f'Process {os.getpid()} done in {t1-t0:.2f} s (found {n} primes in [0, {num}])')
    return n

num_procs = 3
num_samples = 20
#values = [i for i in reversed(range(num_samples))]
values = [1]*num_samples
values[0] = 10
values[2] = 10
values[num_samples-1] = 10
P = UptownFunc()
t0 = time()
results = P.parallelise_function(values, coro_func, num_procs)
t1 = time()
print(f'Done in {t1-t0:.2f} s')
print(results)
