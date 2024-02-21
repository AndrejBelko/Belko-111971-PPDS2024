from time import sleep

from fei.ppds import Thread, Semaphore, print


class Shared:
    """This class represents shared data."""
    def __init__(self, semaphore):
        """Initializes shared data."""
        self.semaphore = semaphore


def sleeping(person):
    """This function simulates sleeping of the person.

    Parameters:
    - person (str): The name of the person sleeping.
    """
    print(f'{person} is sleeping')
    sleep(5)


def hygiene(person):
    """This function simulates person doing hygiene.

    Parameters:
    - person (str): The name of the person doing hygiene.
    """
    print(f'{person} is doing hygiene')
    sleep(2)


def eating(person):
    """This function simulates eating of the person.

    Parameters:
    - person (str): The name of the person eating.
    """
    print(f'{person} is eating')
    sleep(2)


def jano(shared):
    """This function simulates Jano's morning routine."""
    sleeping('Jano')
    hygiene('Jano')
    eating('Jano')
    print('Jano is calling Fero')
    shared.semaphore.signal()


def fero(shared):
    """This function simulates Fero's morning routine."""
    sleeping('Fero')
    hygiene('Fero')
    shared.semaphore.wait()
    print('Fero is answering')
    eating('Fero')
    shared.semaphore.signal()


def main():
    """This function creates the semaphore and threads and run them"""
    semaphore = Semaphore(0)
    shared = Shared(semaphore)
    t1 = Thread(jano, shared)
    t2 = Thread(fero, shared)

    t1.join()
    t2.join()


if __name__ == '__main__':
    main()
