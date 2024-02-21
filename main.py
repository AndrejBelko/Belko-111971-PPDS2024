from time import sleep

from fei.ppds import Thread, Semaphore, print, Mutex

SAVAGE = 7


class Shared:
    """This class represents shared data."""

    def __init__(self, servings, cook_sem, mutex, eating, turnstile1, turnstile2):
        """Initializes shared data."""
        self.servings = servings
        self.cook_sem = cook_sem
        self.mutex = mutex
        self.eating = eating
        self.turnstile1 = turnstile1
        self.turnstile2 = turnstile2


def cook_function(shared):
    """
    This function simulates the cooking.
    :param shared: An instance of Shared class with shared data.
    :return:
    """
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
        shared.eating += 1
        if shared.eating != SAVAGE:
            print(f"Savage {i} come to dinner")
        elif shared.eating == SAVAGE:
            print(f"Savage {i} come to dinner last, everybody is now at dinner.")
            shared.turnstile1.signal(SAVAGE)
        shared.mutex.unlock()
        shared.turnstile1.wait()

        shared.mutex.lock()
        shared.servings -= 1
        if shared.eating != 0:
            print(f"Savage {i} take dish")
        elif shared.servings == 0:
            print(f"Savage {i} take last dish")
            shared.cook_sem.signal()
        shared.eating -= 1
        if shared.eating == 0:
            print(f"Savage {i} is last eating.")
            shared.turnstile2.signal(SAVAGE)
        shared.mutex.unlock()
        shared.turnstile2.wait()
        sleep(2)


def main():
    """This function creates the semaphore and threads and run them"""
    servings = 10
    cook_sem = Semaphore(0)
    mutex = Mutex()
    eating = 0
    turnstile1 = Semaphore(0)
    turnstile2 = Semaphore(0)
    shared = Shared(servings, cook_sem, mutex, eating, turnstile1, turnstile2)

    threads = []

    for i in range(SAVAGE):
        threads.append(Thread(savage, i, shared))

    cook_thread = Thread(cook_function, shared)

    for thread in threads:
        thread.join()

    cook_thread.join()


if __name__ == '__main__':
    main()
