# Zadanie 3
Úlohou v zadaní 3 je implementácia simulácie vláčika na húsenkovej dráhe a jeho pasažierov.
Počet pasažierov je daný premennou N a kapacita húsenkovej dráhy pramennou C. Po uskutočnení jazdy
pasažieri opäť čakajú na jazdu.
### Pravidlá
#### Vláčik:
- môže poňať iba C pasažierov (C<N)
- nemôže vykonať jazdu, ak nenastúpilo C pasažierov
- vyvoláva funkcie *load(), run(), unload()*
#### Pasažier
- vyvoláva funkcie *board()* a *unboard()*
- nemože nastúpiť pokým vláčik neurobí *load()*
- nemože vystúpiť pokým vláčik neurobí *unload()*
## Implementácia
Prvým krokom implementácie bolo vytvorenie dvoch vlastných dátových typov. Ako aj v predchádzajúcich zadaniach
som vytvoril triedy *Shared*. 
```python
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
```
V tejto triede sú opäť vytvorené premenné, ku ktorým budú jednotlivé vlákna počas vykonávania svojich funkcií pristupovať.
*BoardQ, boarded, unboardQ, unboarded* predstavujú semafóry inicializované na hodnotu 0. Semafór *boardQ* signalizuje
vláknam pasažierom, kedy je možný nástup do vláčika. Podobnú funkciu vykonáva aj semafór *unboardQ* avšak pri vystupovaní.
*Boarded* a *unboarded* signalizujú vláčiku, že posledný pasažier nastúpil, respektíve vystúpil z vláčiku. 
Premenné *boardB* a *unboardB* reprezentujú bariéry, signalizujúce nastúpenie/vystúpenie všetkých pasažierov

Druhou triedou bola trieda *Barrier*. Bariéru som využil rovnakú ako v predchádzajúcom zadaní.
```python
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
```
Vlákno si zoberie a zamkne zámok, zvýši počítadlo, ktoré počíta, koľko vlákien je prítomných v bariére. Následne kontroluje,
či už je posledné (či je naplnená kapacita vláčika). Ak nie, vlákno odomkne zámok a čaká na internom semafóre bariéry. Ak 
už bolo posledné vynuluje počítadlo a umožní prechod všetkých vlákien v bariére.
Rozšíril som jej funkcionalitu o rozlišovanie, či ide o nástup alebo výstup cestujúcich z vláčika. Po kontrole podmienky
sa signalizuje príslušnému semafóru, že posledný pasažier nastúpil (*boarded*) alebo vystúpil (*unboarded*).

Ďalším krokom bolo vytvorenie funkcií, simulujúcich jednotlivé udalosti vykonávané vláknom vláčika alebo vláknom pasažierov.
Vytvoril som dva typy funkcií:
- využívajúce parameter *i*
- nevyužívajúce žiadny parameter

Tie, ktoré parameter využívali, simulovali udalosti vykonávané pasažiermi. V paramteri *i* je vždy uložené číslo vlákna.
Príklad funkcie *board(i)* a *unboard(i)*:
```python
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
```
Rovnako je implementovaná aj funkcia *unboard(i)*, ktorá simuluje vystupovanie aktuálneho pasažiera. Ukážka výpisu z funkcií:
```
Passenger 6 is boarding
.
.
.
Passenger 6 is unboarding
```
Druhý typ funkcií simuluje správanie vláčiku. Ukážka funkcií *load(), unload(), run()*:
```
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
```
Funkcie len vypisujú, o ktorú aktuálnu udalosť sa jedná. Ukážky výpisov:
``` 
Passengers are boarding.
.
.
.
Train is running.
Passengers are unboarding.
```

Posledným krokom bolo vytvorenie funkcií, ktoré budú jednotlivé vlákna vykonávať. Vytvoril som funkciu *train(shared)* 
reprezentujúcu správanie vláčiku.
```python
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
```
Vlákno vláčika vykonáva svoju funkciu v cykle. Na začiatku vykoná funkciu *load()* ukázanú vyššie v dokumentácii. Následne
signalizuje semafóru simulujúcemu rad na nástup, že pasažieri môžu nastupovať. Potom čaká na signál posledného pasažiera, že
kapacita vláčika bola naplnená. Ďalej sa simuluje jazdu vláčika. Po jazde sa vykoná funkcia *unload()*, singalizuje sa semafóru,
že je možný výstup a vlákno čaká na vystúpenie všetkých pasažierov. Potom sa celý proces opakuje od začiatku.

Funkcia simulujúca správanie pasažierov má okrem parametra *shared* aj parameter *i*, v ktorom je uložené číslo, o ktorého
pasažiera (vlákno) ide.
```python
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
```
Na začiatku cyklu pasažeir čaká na semafóre, ktorý signalizuje možnosť nástupu na vláčik. Po signalizácii od vlákna vláčika, 
že je možný nástup, sa vykoná funkcia *board(i)* a vlákno sa dostane do bariéry, kde čaká na naplnenie kapacity vláčika.
Po nastúpení posledného pasažiera sa vlákno posunie ďalej a čaká na signalizáciu od vláčika, že môže vystúpiť. Vykoná funkciu
*unboard(i)* a príde na druhú inštanciu bariéry, kde čaká na všetkých pasažierov pokým vystúpia. Keď sa tak stane, proces sa opakuje.

## Zdroje
pdf zo semináru 3