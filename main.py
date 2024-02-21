from time import sleep

from fei.ppds import Thread, Semaphore, print


class Shared:
    """This class represents shared data."""
    def __init__(self, servings, cook):
        """Initializes shared data."""
        self.servings = servings
        self.cook = cook


def main():
    """This function creates the semaphore and threads and run them"""
    servings = 10
    cook = Semaphore(0)
    shared = Shared(servings, cook)


if __name__ == '__main__':
    main()
