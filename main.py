from time import sleep

from fei.ppds import Thread, Semaphore, print, Mutex

SAVAGE = 7


class Shared:
    """This class represents shared data."""

    def __init__(self, servings, cook, mutex, eating, turnstile1, turnstile2):
        """Initializes shared data."""
        self.servings = servings
        self.cook = cook
        self.mutex = mutex
        self.eating = eating
        self.turnstile1 = turnstile1
        self.turnstile2 = turnstile2


def savage(i, shared):
    """
    This function simulates behaviour of savage.
    :param i: Number of savage
    :param shared: An instance of Shared class with shared data.
    :return:
    """

    while True:
        shared.mutex.lock()
        print(f"Savage {i} come to dinner")
        shared.eating += 1
        if shared.eating == SAVAGE:
            print(f"Savage {i} is last, everybody is now at dinner.")
            shared.turnstile1.signal(SAVAGE)
        shared.mutex.unlock()
        shared.turnstile1.wait()

        shared.mutex.lock()
        print(f"Savage {i} take dish")
        shared.servings -= 1
        if shared.servings == 0:
            print(f"Savage {i} take last dish")
            shared.cook.signal()
        shared.eating -= 1
        if shared.eating == 0:
            print(f"Savage {i} is last eating.")
            shared.turnstile2.signal(SAVAGE)
        shared.mutex.unlock()
        shared.turnstile2.wait()


def main():
    """This function creates the semaphore and threads and run them"""
    servings = 10
    cook = Semaphore(0)
    mutex = Mutex()
    eating = 0
    turnstile1 = Semaphore(0)
    turnstile2 = Semaphore(0)
    shared = Shared(servings, cook, mutex, eating, turnstile1, turnstile2)

    threads = []

    for i in range(SAVAGE):
        threads.append(Thread(savage, i, shared))


if __name__ == '__main__':
    main()
