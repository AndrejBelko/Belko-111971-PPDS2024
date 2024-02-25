from fei.ppds import Thread, Semaphore, print, Mutex

SAVAGE = 7
POT_CAPACITY = 10


class Shared:
    """This class represents shared data."""

    def __init__(self, cook_sem, pot, mutex, barrier1, barrier2):
        """Initializes shared data."""
        self.servings = POT_CAPACITY
        self.cook_sem = cook_sem
        self.pot = pot
        self.mutex = mutex
        self.barrier1 = barrier1
        self.barrier2 = barrier2


class Barrier:
    """This class represents a barrier."""

    def __init__(self, ready_cnt, turnstile, mutex):
        """Initializes barrier data."""
        self.turnstile = turnstile
        self.ready_cnt = ready_cnt
        self.mutex = mutex

    def wait(self, string, print_each_thread=False, print_last_thread=False):
        """
        Waits until every thread reaches the barrier
        :param string: string to be printed
        :param print_each_thread: whether to print each thread
        :param print_last_thread: whether to print the last thread
        :return:
        """
        self.mutex.lock()
        self.ready_cnt += 1

        if print_each_thread:
            print(string + str(self.ready_cnt))

        if self.ready_cnt == SAVAGE:
            if print_last_thread:
                print(string)
            self.ready_cnt = 0
            self.turnstile.signal(SAVAGE)

        self.mutex.unlock()
        self.turnstile.wait()


def cook_function(shared):
    """
    This function simulates the cooking.
    :param shared: An instance of Shared class with shared data.
    :return:
    """
    while True:
        shared.cook_sem.wait()
        print("Cooking started.")
        shared.servings = POT_CAPACITY
        shared.pot.signal()


def savage(i, shared):
    """
    This function simulates behaviour of savage.
    :param i: Number of savage
    :param shared: An instance of Shared class with shared data.
    :return:
    """

    while True:

        shared.barrier1.wait(f"Savage {i} come to dinner. We are now ", print_each_thread=True)

        shared.barrier2.wait(f"Savage {i} come to dinner last, everybody is now at dinner.", print_last_thread=True)

        shared.mutex.lock()
        if shared.servings != 0:
            print(f"There are {shared.servings} servings in pot. Savage {i} take dish.")
        elif shared.servings == 0:
            print(f"There are {shared.servings} servings in pot. Savage {i} waiting for full pot.")
            shared.cook_sem.signal()
            shared.pot.wait()
            print(f"There are {shared.servings} servings in pot. Savage {i} take dish.")
        shared.servings -= 1

        shared.mutex.unlock()

        print(f"Savage {i} is eating.")


def main():
    """This function creates barriers, shared and threads and run them"""
    ready_cnt = 0
    turnstile = Semaphore(0)
    barrier_mutex = Mutex()
    barrier1 = Barrier(ready_cnt, turnstile, barrier_mutex)

    ready_cnt2 = 0
    turnstile2 = Semaphore(0)
    barrier_mutex2 = Mutex()
    barrier2 = Barrier(ready_cnt2, turnstile2, barrier_mutex2)

    mutex = Mutex()
    cook_sem = Semaphore(0)
    pot = Semaphore(0)
    shared = Shared(cook_sem, pot, mutex, barrier1, barrier2)

    threads = []

    for i in range(SAVAGE):
        threads.append(Thread(savage, i, shared))

    cook_thread = Thread(cook_function, shared)

    for thread in threads:
        thread.join()

    cook_thread.join()


if __name__ == '__main__':
    main()
