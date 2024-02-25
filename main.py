from fei.ppds import Thread, Semaphore, print, Mutex

SAVAGE = 7
POT_CAPACITY = 10


class Shared:
    """This class represents shared data."""

    def __init__(self, cook_sem, mutex, pot, barrier):
        """Initializes shared data."""
        self.servings = POT_CAPACITY
        self.cook_sem = cook_sem
        self.mutex = mutex
        self.pot = pot
        self.barrier = barrier


class Barrier:
    """This class"""
    def __init__(self, ready_cnt, turnstile):
        """Initializes barrier data."""
        self.turnstile = turnstile
        self.ready_cnt = ready_cnt

    def wait(self):
        """Waits until"""


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
        shared.mutex.lock()
        shared.ready_cnt += 1
        if shared.ready_cnt != SAVAGE:
            print(f"Savage {i} come to dinner. There are already {shared.ready_cnt} of us")
        elif shared.ready_cnt == SAVAGE:
            print(f"Savage {i} come to dinner last, everybody is now at dinner.")
            shared.ready_cnt = 0
            shared.turnstile1.signal(SAVAGE)
            print()
        shared.mutex.unlock()
        shared.turnstile1.wait()

        shared.mutex.lock()
        shared.servings -= 1
        if shared.servings != 0:
            print(f"Savage {i} take dish. There are {shared.servings} servings in pot.")
        elif shared.servings == 0:
            print(f"Savage {i} take last dish. There is no serving in pot.")
            shared.cook_sem.signal()
            shared.pot.wait()

        shared.ready_cnt += 1
        if shared.ready_cnt == SAVAGE:
            shared.ready_cnt = 0
            shared.turnstile2.signal(SAVAGE)
            print()
        shared.mutex.unlock()
        shared.turnstile2.wait()

        print(f"Savage {i} is eating.")


def main():
    """This function creates semaphores, shared and threads and run them"""
    ready_cnt = 0
    turnstile = Semaphore(0)
    barrier = Barrier(ready_cnt, turnstile)

    cook_sem = Semaphore(0)
    mutex = Mutex()
    pot = Semaphore(0)
    shared = Shared(cook_sem, mutex, pot, barrier)

    threads = []

    for i in range(SAVAGE):
        threads.append(Thread(savage, i, shared))

    cook_thread = Thread(cook_function, shared)

    for thread in threads:
        thread.join()

    cook_thread.join()


if __name__ == '__main__':
    main()
