from time import sleep

from fei.ppds import Thread, Semaphore, print, Mutex

SAVAGE = 7


class Shared:
    """This class represents shared data."""

    def __init__(self, servings, cook_sem, mutex, ready_cnt, turnstile1, turnstile2):
        """Initializes shared data."""
        self.servings = servings
        self.cook_sem = cook_sem
        self.mutex = mutex
        self.ready_cnt = ready_cnt
        self.turnstile1 = turnstile1
        self.turnstile2 = turnstile2


def cook_function(shared):
    """
    This function simulates the cooking.
    :param shared: An instance of Shared class with shared data.
    :return:
    """
    while True:
        shared.cook_sem.wait()
        print("Cooking started.")
        shared.servings = 10


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
        sleep(1)
        shared.ready_cnt += 1
        if shared.ready_cnt == SAVAGE:
            shared.ready_cnt = 0
            shared.turnstile2.signal(SAVAGE)
            print()
        shared.mutex.unlock()
        shared.turnstile2.wait()

        print(f"Savage {i} is eating.")
        sleep(2)


def main():
    """This function creates semaphores, shared and threads and run them"""
    servings = 10
    cook_sem = Semaphore(0)
    mutex = Mutex()
    ready_cnt = 0
    turnstile1 = Semaphore(0)
    turnstile2 = Semaphore(0)
    shared = Shared(servings, cook_sem, mutex, ready_cnt, turnstile1, turnstile2)

    threads = []

    for i in range(SAVAGE):
        threads.append(Thread(savage, i, shared))

    cook_thread = Thread(cook_function, shared)

    for thread in threads:
        thread.join()

    cook_thread.join()


if __name__ == '__main__':
    main()
