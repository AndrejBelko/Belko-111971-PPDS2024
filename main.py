import threading

from fei.ppds import Thread, Semaphore, print, Mutex

class Shared:
    def __init__(self):
        self.semaphore = Semaphore()
        self.mutex = Mutex()


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

def main():
    print("Hello World!")


if __name__ == '__main__':
    main()
