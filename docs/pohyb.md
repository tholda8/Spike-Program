# Pohyb robota, gyro a jízda rovně

Tento projekt používá vlastní jednoduchou odometrii. Poloha robota se drží v `drive.robot.pos` jako `vec2(x, y)` a směr robota se bere z gyra v hubu. Díky tomu můžeš řídit robota v souřadnicích, ne jen podle času běhu motorů.

## 1. Souřadnicový systém

Souřadnice jsou vedené v rovině hřiště:

- `x` je směr doprava / doleva podle mapy úlohy
- `y` je směr nahoru / dolů podle mapy úlohy
- orientace robota je úhel v radiánech nebo ve stupních

Startovní poloha se typicky nastavuje ručně v `setup.py` nebo v konkrétním scénáři, například:

```python
drive.robot.pos = vec2(15, 8)
drive.robot.hub.resetAngle()
drive.robot.hub.addOffset(-90)
```

`resetAngle()` uloží aktuální orientaci hubu jako novou nulu a `addOffset()` posune referenci. To je důležité hlavně tehdy, když robot startuje otočený proti jinému směru, než je běžná osa souřadnic.

## 2. Jak se počítá poloha robota

Skutečný posun robota se počítá v metodě `update()` instance třídy `Robot`.

Tato metoda volá `navigate(...)` v [robot.py](../spike/spike_lib/robot.py), která udělá toto:

1. vezme změnu natočení levého a pravého kola od poslední aktualizace
2. z těchto změn spočítá přibližný posun dopředu
3. ten posun otočí podle aktuálního úhlu gyra
4. výsledný vektor přičte k `robot.pos`

Tím je pohyb robota v prostoru vázaný na skutečný směr těla robota, ne jen na lokální osu motorů.

Prakticky to znamená, že když robot jede dopředu a je lehce vytočený, další aktualizace posune jeho souřadnici už ve správném směru v mapě.

## 3. Jak funguje gyro

V [robot.py](../spike/spike_lib/robot.py) je třída `Hub`. V příkladech níže je `hub` její instance uložená v objektu `Robot`.

- `hub.angle()` vrací orientaci z IMU v stupních
- `hub.angleRad()` vrací totéž v radiánech
- `hub.addOffset(...)` přidá ruční korekci nulového směru
- `hub.resetAngle()` nastaví novou nulu podle aktuální orientace

To je základ celého souřadnicového řízení. Když je gyro správně zkalibrované, všechny další výpočty už pracují v jednom konzistentním prostoru.

## 4. Jízda na bod

Nejdůležitější funkce je `drive.toPos(...)` v [driveFunc.py](../spike/spike_lib/driveFunc.py).

Zjednodušeně funguje takto:

1. vezme aktuální polohu robota
2. spočítá úhel k cílovému bodu přes `atan2(...)`
3. případně robota natočí tímto směrem přes `rotateRad(...)`
4. pak v cyklu opakovaně aktualizuje pozici a hlídá, jestli je robot pořád na přímce k cíli
5. podle chyby směru upravuje rychlost levého a pravého motoru přes `calcDir(...)`

`calcSpeed(...)` současně hlídá, jak rychle má robot jet. Na začátku dovolí větší zrychlení, u cíle začne brzdit. Tím se snižuje přestřelování a robot dojíždí plynuleji.

### Režim couvání

Když je `backwards=True`, funkce nejdřív přizpůsobí směr jízdy a potom při řízení motorů obrátí znaménka. Robot tedy couvá, ale pořád se řídí podle stejné cílové souřadnice.

### Režim `background`

Pokud je `background=True`, pohyb se nepustí hned blokující smyčkou, ale uloží se jako úloha do `drive.tasks`. Pak ji lze posouvat přes `drive.runTasks()` společně s dalšími úlohami.

## 5. Jízda rovně

`drive.straight(length, ...)` je jen zkrácená vrstva nad `toPos(...)`.

V [driveFunc.py](../spike/spike_lib/driveFunc.py) je implementace:

```python
def straight(self, length, speed = 1000, backwards = False, background = False):
    self.toPos(self.robot.pos + mat2.rotation(self.robot.hub.angleRad()) * vec2(length,0), speed, backwards, background=background)
```

To znamená:

1. vezme aktuální pozici robota
2. vezme jeho aktuální směr z gyra
3. vytvoří vektor délky `length` ve směru, kam robot kouká
4. přičte ho k aktuální poloze
5. a pak jen zavolá jízdu na výsledný bod

Jízda rovně je tedy ve skutečnosti speciální případ jízdy na souřadnici. Není to samostatný motorový režim.

## 6. Co přesně drží robota na přímce

Při jízdě na bod se robot nespoléhá jen na to, že „jede oba motory stejně“.

`calcDir(...)` porovnává:

- skutečný úhel robota z gyra
- ideální směr k cíli

Podle rozdílu pak upraví rychlost levého a pravého motoru. Když je robot vychýlený doleva, zpomalí jednu stranu a druhou ponechá rychlejší, aby se vrátil na přímku.

To je důvod, proč robot umí držet směr i při drobném skluzu kol nebo při nerovném povrchu.

## 7. Kde se to typicky ladí

Pokud robot v praxi ujíždí, kontroluj hlavně:

- `r.lM.reverse` a `r.rM.switchDir` v `setup.py`
- nulový úhel přes `drive.robot.hub.addOffset(...)`
- startovní polohu `drive.robot.pos`
- parametry režimu `setPreciseMode()`, `setFastMode()` a `setDefaultMode()`

Pokud robot po otočení míří správně, ale při jízdě na bod se stáčí, problém je většinou v parametrech řízení, tedy v `acc`, `deacc`, `turnCoeff` nebo v kalibraci gyra.

## 8. Krátké shrnutí

- gyro dává absolutní směr robota
- odometrie z kol dává změnu polohy
- `robot.update()` tyto dvě věci propojí do nové globální pozice
- `toPos()` drží robotovu osu na cílovém směru
- `straight()` je jen pohodlný wrapper nad `toPos()`
