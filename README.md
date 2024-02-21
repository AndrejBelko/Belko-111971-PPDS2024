# Zadanie 1

Implementujte problém „Kto raňajkoval skôr“ z prednášky. Simulujte procesy spánok, ranná hygiena, telefonát, raňajky.
Zabezpečte, aby subjekt A (nazvime ho Jano) raňajkoval skôr ako
subjekt B (nazvime ho Fero). Inšpirujte sa schémou z prednášky. Spíšte dokumentáciu. V nej uveďte všetky podstatné detaily
o implementácii. Súčasťou dokumentácie musia byť aj výpisy
z konzoly.

## Implementácia
Prvým krokom bolo vytvorenie funkcií simulujúcich jednotlivé udalosti. Každá z funkcií pozostávala z výpisu mena osoby, 
ktorá danú činnosť vykonáva. To som zabezpečil posielaním reťazca s menom ako parameter do funkcie. Ďalším krokom vo funkcii
bolo vykonanie príkazu *sleep()* na určitý počet sekúnd. Príklad funkcie simulujúcej spánok osoby:
```python
def sleeping(person):
    print(f'{person} is sleeping')
    sleep(5)
```
Výpis z tejto funkcie zavolanej s parametrom *person = 'Jano'* vyzeral takto:
```
Jano is sleeping
```

Pri volaní funkcii *main()* som vytvoril semafór, incializovaný na hodnotu 0. Následne som vytvoril inštanciu triedy *Shared*,
ktorú tvoril iba semafór. Potom som vytvoril 2 vlákna s funkciami *jano* a *fero*, ktorých argumentom bola vytvorená trieda
*Shared*. Ukážka funkcie *main()*:

```python
def main():
    semaphore = Semaphore(0)
    shared = Shared(semaphore)
    t1 = Thread(jano, shared)
    t2 = Thread(fero, shared)

    t1.join()
    t2.join()
```

Ďalším krokom bolo vytvorenie funkcií simulújucich celú rannú rutinu pre Jana a Fera, ktoré boli priradené vytvoreným vláknam. Tieto dve funkcie boli rozdielne z 
dôvodu, že Jano mal raňajkovať ako prvý, následne mal zavolať Ferovi, ktorý až po prijatí telefonátu mohol začať raňajkovať.
Úkažka Janovej funkcie:

```python
def jano(shared):
    sleeping('Jano')
    hygiene('Jano')
    eating('Jano')
    print('Jano is calling Fero')
    shared.semaphore.signal()

```
Po vykonaní funkcií *sleeping(), hygiene(), eating()* nasledoval výpis *print('Jano is calling Fero')*, signalizujúci, že Jano
skončil s rannou rutinou. Následne sa vykonala funkcia *semaphore.singal()*, ktorá zvýšila hodnotu semafóru na 1.

Funkcia *fero* vyzerala podobne ako funkcia *jano*. Rozdielom bolo, že funkciu *eating()* predchádzalo volanie *semaphore.wait()*,
čo zabezpečilo, že vlákno čakalo na zvýšenie hodnoty semafóru z druhého vlákna.

```python
def fero(shared):
    sleeping('Fero')
    hygiene('Fero')
    shared.semaphore.wait()
    print('Fero is answering')
    eating('Fero')
    shared.semaphore.signal()
```
Keď vlákno Jano dalo signál semafóru (po ukončení raňajkovania), vlákno Fero mohlo ďalej pokračovať (raňajkovať). Použitím
semafóru bol dosiahnutý cieľ zadania. 

Konečný výpis programu po behu č. 1:
```
Jano is sleeping
Fero is sleeping
Fero is doing hygiene
Jano is doing hygiene
Jano is eating
Jano is calling Fero
Fero is answering
Fero is eating
```

Konečný výpis programu po behu č. 2:
``` 
Jano is sleeping
Fero is sleeping
Jano is doing hygiene
Fero is doing hygiene
Jano is eating
Jano is calling Fero
Fero is answering
Fero is eating
```
Rozdiel medzi behom č. 1 a behom č. 2 je, že v prvom behu funkciu *hygiene()* najprv vykoná vlákno 
Fero, pri druhom behu je to vlákno Jano. To je dôkaz o konkurentnom behu programu.

## Zdroje
https://github.com/tj314/ppds-seminars/blob/ppds2024/seminar1/semaphore_example.py
https://elearn.elf.stuba.sk/moodle/pluginfile.php/77036/mod_resource/content/1/PPDS_seminar_01_2024.pdf
https://www.dataquest.io/blog/documenting-in-python-with-docstrings/