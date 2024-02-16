from fei.ppds import Thread, Semaphore, print


class Shared:
    def __init__(self, semaphore):
        self.semaphore = semaphore


def main():
    semaphore = Semaphore(0)
    shared = Shared(semaphore)
    t1 = Thread()
    t2 = Thread()

    t1.join()
    t2.join()


if __name__ == '__main__':
    main()
