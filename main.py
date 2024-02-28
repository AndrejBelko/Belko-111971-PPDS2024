import threading

from fei.ppds import Thread, Semaphore, print, Mutex


class Shared:
    def __init__(self, boardQ, boarded, unboardQ, unboarded, boardB, unboardB):
        self.boardQ = boardQ
        self.boarded = boarded
        self.unboardQ = unboardQ
        self.unboarded = unboarded
        self.boardB = boardB
        self.unboardB = unboardB


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


def load():
    print("Passengers are boarding.")


def unload():
    print("Passengers are unboarding.")


def run():
    print("Train is running.")


def board(i):
    print(f"Passenger {i} is boarding")


def unboard(i):
    print(f"Passenger {i} is unboarding")


def train(shared):
    """Train the """
    while True:
        load()
        shared.boardQ.signal(C)
        shared.boarded.wait()

        run()

        unload()
        shared.unboardQ.signal(C)
        shared.unboarded.wait()


def passenger(i, shared):
    """Passenger """
    while True:
        shared.boardQ.wait()
        board()
        shared.boardB.wait(shared.boarded.signal())  # bariera

        shared.unboardQ.wait()
        unboard()
        shared.unboardB.wait(shared.unboarded.signal())  # bariera


def main():
    """Main function"""
    boardQ = Semaphore(0)
    boarded = Semaphore(0)
    unboardQ = Semaphore(0)
    unboarded = Semaphore(0)

    ready_cnt = 0
    turnstile = Semaphore(0)
    barrier_mutex = Mutex()
    boardB = Barrier(ready_cnt, turnstile, barrier_mutex)

    ready_cnt2 = 0
    turnstile2 = Semaphore(0)
    barrier_mutex2 = Mutex()
    unboardB = Barrier(ready_cnt2, turnstile2, barrier_mutex2)

    shared = Shared(boardQ, boarded, unboardQ, unboarded, boardB, unboardB)


if __name__ == '__main__':
    main()
