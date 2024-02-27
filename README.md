# Zadanie 1
Divosi v Rovníkovej Guinei sú veľmi spoločenský a vyspelý typ divochov.
Nielen, že každý deň jedia vždy spolu, ale majú medzi sebou aj šikovného
kuchára, ktorý pripravuje výborný guláš zo zebry. Potrebujú však spoľahlivý
systém, v ktorom budú oznamovať všetky úkony, ktoré so spoločným
hodovaním súvisia.
- Divosi vždy začínajú jesť spolu. Posledný divoch, ktorý príde, všetkým
signalizuje, že sú všetci a začať môžu hodovať.
- Divosi si po jednom berú svoju porciu z hrnca dovtedy, kým nie je
hrniec prázdny.
- Divoch, ktorý zistí, že už je hrniec prázdny upozorní kuchárov, aby
znovu navarili.
- Divosi čakajú, kým kuchári doplnia plný hrniec.
- Kuchár vždy navarí jednu porciu a vloží ju do hrnca.
- Keď je hrniec plný, divosi pokračujú v hodovaní.
- Celý proces sa opakuje v nekonečnom cykle.

## Implementácia
V mojej implementácií využívam dva, mnou vytvorené dátové typy *Shared* a *Barrier*. Používam tiež globálne premenné 
*SAVAGE* v ktorej je uložený počet divochov (vlákien) v našom prípade nastavený na počet 7 a *POT_CAPACITY*, 
kde je uložená maximálna kapacity hrnca rovná 10. 

V triede *Shared* sú uložené premenné, ktoré priamo súvisia s večerou. Ukážka triedy *Shared*:
```python
class Shared:
    """This class represents shared data."""

    def __init__(self, cook_sem, pot, mutex, barrier1, barrier2):
        """Initializes shared data."""
        self.servings = POT_CAPACITY
        self.cook_sem = cook_sem
        self.pot = pot
        self.mutex = mutex
        self.barrier1 = barrier1
        self.barrier2 = barrier2
```
Premenná *servings* ukladá údaj o tom, koľko porcií je ešte dostupných v hrnci. Ďalšie dve premnné *cook_sem* a *pot* sú
semafóry. Ich funkcia bude vysvetlená ďalej v dokumentácii, ako aj funkcia premennej *mutex*. Posledné dve premnné *barrier1* 
a *barrier2* sú dátového typu *Barrier* a služia na sychronizáciu vlákien a tiež ich priblížim neskôr.

V triede *Barrier* sú uložené premenné, ktoré som pri implementácii využíval na zabezpečenie synchronizácie. Ukážka triedy
*Barrier*:
```python
class Barrier:
    """This class represents barrier."""

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
```
V tejto triede využívam premenné *turnstile*, v ktorej je uložený semafór, *ready_cnt* čo predstavuje počítadlo bariéry a 
*mutex* čo je zámok využívaný v bariére.

Taktiež som implementoval jednu metódu *wait()*, ktorá zabezpečuje spomínanú syncrhonizáciu. Metóda má ako vstupné parametre
*string*, kde je uložený reťazec, ktorý sa mý vypísať, *print_each_thread* a *print_last_thread* implicitne nastavené
na hodnotu *False*. Tieto hodnoty v prípade potreby pri volaní nastavujem na hodnotu *True*. Ide znovupoužiteľnú bariéru 
z prednášky. Znovupoužiteľná sa nazýva z dôvodu vykonania rovnakej funkcionality viacnásobne v kóde.
### Funkcionalita bariéry
Vlákno, ktoré zavolá metódu *wait()* pre daný objekt bariéry si následne zoberie jej zámok, zvýši počítadlo o 1, následne 
skontroluje, či má uskutočniť aj výpis a či aktuálne vlákno je posledné. Ak nie je posledné tak uvoľní zámok a čaka na posledné vlákno.
Keď posledné vlákno príde, vynuluje počítadlo a nastaví semafór na hodnotu rovnú globálnej premnnej *SAVAGE*. Potom uvoľní
zámok a môže spolu s ostatnými vláknami prejsť semafórom. 


Ďalším krokom bolo implementovanie funkcie, ktorú bude vykonávať vlákno *Cook*. Funkcia je jednoduchý *while* cyklus, 
ktorý na začiatku čaká na signál semafóru uloženého v triede *Shared*. Následne sa vypíše reťazec *"Cooking started"*, 
zvýši sa počet porcií na 10 a ako posledný krok dá signál semafóru signalizujúcemu naplnenie hrnca. Ukážka funkcie pre 
vlákno kuchára:
```python
def cook_function(shared):
    """
    This function simulates the cooking.
    :param shared: An instance of Shared class with shared data.
    :return:
    """
    while True:
        shared.cook_sem.wait()
        print("Cooking started.")
        shared.servings = POT_CAPACITY
        shared.pot.signal()
```

Podobne ako pre vlákno kuchára som implementoval aj funckiu pre vlákno divocha. Ukážka funkcie pre vlákno divochov:
```python
def savage(i, shared):
    """
    This function simulates behaviour of savage.
    :param i: Number of savage
    :param shared: An instance of Shared class with shared data.
    :return:
    """

    while True:

        shared.barrier1.wait(f"Savage {i} come to dinner. We are now ", 
                             print_each_thread=True)

        shared.barrier2.wait(f"Savage {i} come to dinner last, everybody is now at dinner.", 
                             print_last_thread=True)

        shared.mutex.lock()
        if shared.servings != 0:
            print(f"There are {shared.servings} servings in pot. Savage {i} take dish.")
        elif shared.servings == 0:
            print(f"There are {shared.servings} servings in pot. Savage {i} waiting for full pot.")
            shared.cook_sem.signal()
            shared.pot.wait()
            print(f"There are {shared.servings} servings in pot. Savage {i} take dish.")
        shared.servings -= 1

        shared.mutex.unlock()

        print(f"Savage {i} is eating.")
```
Funkcia má dva parametre: 
- *i*: číslo vlákna
- *shared*: zdieľaná pamäť

Správanie divocha tiež prebieha v cykle. Na začiatku divoch čaká na ostatných divochov na prvej bariére. Po príchode posledného
sa presunú na druhú bariéru, ktorá zabraňuje predbiehaniu vlákien. Následne sa všetci vypustia na večeru. Tá prebieha tak,
že aktuálne vlákno si zoberie a zamkne zámok. Do tejto oblasti nemá žiadne iné vlákno prístup. Vlákno odpočíta počítadlo
porcií, ak ešte nie je počet porcií rovný 0, vypíše, koľko porcií zostáva. Ak vlákno, ktoré príde, zistí, že počet porcií
je rovný 0, dá signál kuchárovi, ktorý doplní hrniec a signalizuje jeho akciu aby vlákno divocha mohlo ďalej pokračovať v hodovaní.
Posledné kroky sú odčítanie počtu porcií, uvoľnenie zámku a vypís, že aktuálny divoch hoduje.

## Výpisy
Po spustení programu všetci divosi čakajú na posledného, ktorý príde na večeru.
```
Savage 0 come to dinner. We are now 1
Savage 1 come to dinner. We are now 2
Savage 2 come to dinner. We are now 3
Savage 3 come to dinner. We are now 4
Savage 4 come to dinner. We are now 5
Savage 5 come to dinner. We are now 6
Savage 6 come to dinner. We are now 7
Savage 3 come to dinner last, everybody is now at dinner.
```
V tomto prípade divoch, ktorý prišiel posledný si ako prvý berie jedlo, hoduje a znovu prichádza na večeru, kde čaká na 
ostatných.
```
Savage 3 come to dinner last, everybody is now at dinner.
There are 10 servings in pot. Savage 3 take dish.
Savage 3 is eating.
Savage 3 come to dinner. We are now 1

```
Nasledujúci výpis zobrazuje prípad, keď je počet porcií v hrnci rovný 0.

```
There are 1 servings in pot. Savage 5 take dish.
Savage 5 is eating.
Savage 5 come to dinner. We are now 3
There are 0 servings in pot. Savage 1 waiting for full pot.
Cooking started.
There are 10 servings in pot. Savage 1 take dish.
Savage 1 is eating.
Savage 1 come to dinner. We are now 4
```
Divoch 5 si zoberie poslednú porciu, hoduje, ide naspäť na večeru. Nasledujúce vlákno divocha 1 zistí, že hrniec je prázdny,
to signalizuje kuchárovi. Čaká na naplnenie hrnca, potom si zoberie porciu, hoduje a presunie sa naspäť na začiatok.

Vlákno, ktoré príde ako posledné na prvú bariéru nemusí prísť aj posledné na druhú bariéru. Preto výpis môže vyzerať aj 
takto:
```
Savage 2 come to dinner. We are now 7
Savage 4 come to dinner last, everybody is now at dinner.
There are 9 servings in pot. Savage 4 take dish.
```

## Synchornizačné vzory
### Mutex
Zabezpečenie aby v jednom čase pristupovalo k zdieľanej pamäti len jedno vlákno. 
Príklad: Zniženie počtu porcií v hrnci keď si divoch zoberie jedlo.
```python
shared.mutex.lock()
if shared.servings != 0:
    print(f"There are {shared.servings} servings in pot. Savage {i} take dish.")
elif shared.servings == 0:
    print(f"There are {shared.servings} servings in pot. Savage {i} waiting for full pot.")
    shared.cook_sem.signal()
    shared.pot.wait()
    print(f"There are {shared.servings} servings in pot. Savage {i} take dish.")
shared.servings -= 1
shared.mutex.unlock()
```

### Semafór
Semafór je celočíselná premenná zdieľaná medzi viacerými procesmi. Na rozdiel od mutexu, prístup do kritickej oblasti môže
povoliť iné vlákno (napr. také, ktoré do oblasti nevstupuje).
Príklad: Signalizácia kuchárovi, že hrniec je prázdny. Signalizácia divochom, že hrniec je plný.
```python
print(f"There are {shared.servings} servings in pot. Savage {i} waiting for full pot.")
shared.cook_sem.signal()
shared.pot.wait()
```
### Turniket
Turniket je semafór, ktorý umožňuje prechod všetkých vlákien cez bariéru. Implementácia je zobrazená pri ukážke kódu triedy
*Barrier* vyššie v dokumentácii.

### Bariéra
Ukážka implementácie bariéry je zobrazená vyššie v dokumentácii. Slúži na zosychronizovanie, stretnutie všetkých vlákien na 
jednom mieste v kóde.

### Znovupoužiteľná bariéra 
Bariéra, ktorá vykonavá rovnakú funkciu a je použiteľná na viacerých miestach v programe.

```python
shared.barrier1.wait(f"Savage {i} come to dinner. We are now ", print_each_thread=True)

shared.barrier2.wait(f"Savage {i} come to dinner last, everybody is now at dinner.", print_last_thread=True)
```






## Zdroje
https://elearn.elf.stuba.sk/moodle/pluginfile.php/77190/mod_resource/content/1/PPDS_seminar_02_2024.pdf
https://elearn.elf.stuba.sk/moodle/pluginfile.php/77169/mod_resource/content/2/2024-02.mutex%20multiplex%20randezvouse%20bariera.pdf
