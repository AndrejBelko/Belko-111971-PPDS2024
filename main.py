from time import sleep

from fei.ppds import Thread, Semaphore, print


class Shared:
    def __init__(self, semaphore):
        self.semaphore = semaphore


def sleeping(person):
    print(f'{person} is sleeping')
    sleep(5)


def hygiene(person):
    print(f'{person} is doing hygiene')
    sleep(2)


def eating(person):
    print(f'{person} is eating')
    sleep(2)


def jano():
    sleeping('Jano')
    hygiene('Jano')
    eating('Jano')


def fero():
    sleeping('Fero')
    hygiene('Fero')
    eating('Fero')


def main():
    semaphore = Semaphore(0)
    shared = Shared(semaphore)
    t1 = Thread(jano, shared)
    t2 = Thread(fero, shared)

    t1.join()
    t2.join()


if __name__ == '__main__':
    main()
