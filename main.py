from fei.ppds import Thread, Semaphore, print, Mutex

C = 5
N = 10


class Shared:
    """Shared variables."""
    def __init__(self, boardQ, boarded, unboardQ, unboarded, boardB, unboardB):
        """Initialize shared variables."""
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

    def wait(self, shared=None, unboard=False, board=False):
        """
        Waits until every thread reaches the barrier
        :param board: barrier is used while passengers are boarding
        :param unboard: barrier is used while passengers are unboarding
        :param shared: shared data
        :return:
        """
        self.mutex.lock()
        self.ready_cnt += 1

        if self.ready_cnt == C:
            if unboard:
                shared.unboarded.signal()
            if board:
                shared.boarded.signal()
            self.ready_cnt = 0
            self.turnstile.signal(C)

        self.mutex.unlock()
        self.turnstile.wait()


def load():
    """
    This function simulates boarding passengers.
    :return:
    """
    print("Passengers are boarding.")


def unload():
    """
    This function simulates unboarding passengers.
    :return:
    """
    print("Passengers are unboarding.")


def run():
    """
    This function simulates train ride.
    :return:
    """
    print("Train is running.")


def board(i):
    """
    This function simulates boarding of specific passenger.
    :param i: number (id) of passengers being boarded.
    :return:
    """
    print(f"Passenger {i} is boarding")


def unboard(i):
    """
    This function simulates unboarding of specific passenger.
    :param i: number (id) of passenger being unboarded.
    :return:
    """
    print(f"Passenger {i} is unboarding")


def train(shared):
    """
    This function represents behaviour of train.
    :param shared: shared data
    :return:
    """
    while True:
        load()
        shared.boardQ.signal(C)
        shared.boarded.wait()

        run()

        unload()
        shared.unboardQ.signal(C)
        shared.unboarded.wait()


def passenger(i, shared):
    """
    This function represents behaviour of passenger.
    :param i: number (id) of passenger
    :param shared: shared data
    :return:
    """
    while True:
        shared.boardQ.wait()
        board(i)
        shared.boardB.wait(shared, board=True)

        shared.unboardQ.wait()
        unboard(i)
        shared.unboardB.wait(shared, unboard=True)


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

    threads = []

    for i in range(N):
        threads.append(Thread(passenger, i, shared))

    train_thread = Thread(train, shared)

    for thread in threads:
        thread.join()

    train_thread.join()


if __name__ == '__main__':
    main()
