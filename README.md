# Spike Prime robot codebase

Tento repozitář obsahuje řízení robota pro LEGO SPIKE Prime, menu na hubu a několik samostatných soutěžních režimů. Základní myšlenka je jednoduchá: `setup.py` vytvoří robota a `driveFunc.py` pak řeší pohyb, otáčení, jízdu na souřadnici a běh více úloh najednou.

## Co je tady za co odpovědné

- `main.py` - spouští menu a vybírá jednotlivé scénáře.
- `setup.py` - skládá konkrétního robota, motorové směry a instanci třídy `DriveManager` (uloženou v proměnné `drive`).
- `robot.py` - nízkoúrovňové obaly nad motory, hubem, senzory a odometrií.
- `driveFunc.py` - hlavní vrstva pro pohyb: otočení, jízda na bod, jízda rovně, kružnice a plánování úloh na pozadí.
- `maths.py` - vektory, matice, PID a pomocné funkce.
- `vyzva.py`, `vyzvajesenik*.py`, `wro.py`, `roadside.py` - konkrétní strategie a sekvence pro soutěže.

## Jak se projekt používá

1. Otevři `main.py` jako vstupní bod.
2. Vyber režim přes menu na hubu.
3. Každý režim volá pohybové funkce z `driveFunc.py`, které pracují s globální pozicí robota `drive.robot.pos` a s úhlem z gyra.

V `setup.py` je základní konfigurace robota:

- levý a pravý motor jsou vytvořené jako `Robot(Port.E, Port.F, 5.8, 11.2)`
- levý motor je obrácený přes `r.lM.reverse = True`
- osa a nulový úhel se pak doladí přes `r.hub.addOffset(...)`

## Jak funguje pohyb

Pohyb je postavený na dvou vrstvách:

- odometrie počítá aktuální pozici z natočení kol
- gyro určuje absolutní směr robota v prostoru

To znamená, že robot si vede vlastní souřadnicový systém. Když je poloha správně zkalibrovaná, můžeš volat například `drive.toPos(vec2(60, 40))` a robot se snaží dojet na daný bod bez ohledu na to, jak je natočený.

Podrobné vysvětlení je v [docs/pohyb.md](docs/pohyb.md).

## Důležité funkce pro pohyb

- `drive.rotate(angle)` a `drive.rotateRad(angle)` - otočení na zadaný úhel.
- `drive.toPos(pos)` - jízda na konkrétní souřadnici.
- `drive.straight(length)` - jízda rovně ve směru aktuálního gyra.
- `drive.circleToPos(...)` - obloukový přechod mezi body.
- `drive.runTasks()` - posouvá dopředu úlohy spuštěné na pozadí.

## Ladění a kalibrace

Pokud robot ujíždí mimo osu, nejčastěji pomůže:

- zkontrolovat `reverse` a `switchDir` v `setup.py`
- přenastavit `drive.robot.hub.addOffset(...)`
- upravit `drive.robot.pos` v místě, kde je poloha známá
- přepnout režim `setPreciseMode()`, `setDefaultMode()` nebo `setFastMode()` podle úlohy

## Dokumentace

- [Pohyb a gyro odometrie](docs/pohyb.md)
