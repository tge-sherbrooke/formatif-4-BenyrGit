# Formatif F4 — Timer et Bouton Polling Python

**Cours** : 243-413-SH — Introduction aux objets connectes
**Semaine** : 4
**Type** : Formative (non notee)
**Retries** : Illimites - poussez autant de fois que necessaire!

---

> **Pratique autonome** -- Ce formatif est une evaluation formative (non notee). Contrairement au laboratoire guide, vous devez completer les taches de maniere autonome. Les tests automatiques vous donnent une retroaction immediate a chaque push.

## Ce que vous avez appris en labo

Le laboratoire de la semaine 4 vous a guide a travers :

- Structuration d'un script Python avec fonctions et main guard
- Utilisation de `time.monotonic()` pour des timers non-bloquants
- Pattern timer-in-loop pour executer des actions a intervalles reguliers
- Lecture d'un bouton par polling digitalio dans la boucle principale
- Arret propre avec `break` et `finally`

Ce formatif vous demande d'appliquer ces competences de maniere autonome.

---

## Progressive Milestones

Ce formatif utilise des **jalons progressifs** avec retroaction detaillee:

| Jalon | Points | Verification |
|-------|--------|-------------|
| **Milestone 1** | 25 pts | Script main.py, garde `__main__`, fonctions, constantes |
| **Milestone 2** | 35 pts | Imports time, utilisation `time.monotonic()`, pattern timer-in-loop |
| **Milestone 3** | 40 pts | digitalio bouton polling, `break` pour arret, gestion erreurs |

**Chaque test echoue vous dit**:
- Ce qui etait attendu
- Ce qui a ete trouve
- Une suggestion pour corriger

---

## Objectif

Ce formatif vise a verifier que vous etes capable de :
1. Structurer du code Python avec des fonctions et un garde main
2. Utiliser `time.monotonic()` pour des timers non-bloquants dans une boucle
3. Detecter le bouton par polling avec digitalio dans la boucle principale
4. Gerer proprement l'arret du programme (maintien du bouton + Ctrl+C)

---

## Le probleme a resoudre

**Scenario**: Votre superviseur a remarque un probleme avec votre code de la semaine 3:

> "Quand tu appuies sur le bouton pendant que le capteur est en lecture,
> rien ne se passe. Le programme est bloque par `time.sleep(5)`!"

**Solution**: Le pattern timer-in-loop avec `time.monotonic()` permet de:
- Lire les capteurs a intervalles reguliers SANS bloquer
- Detecter les appuis bouton immediatement dans la meme boucle
- Arreter proprement en maintenant le bouton

---

## Workflow de soumission

```
+-------------------------------------------------------------+
|                    WORKFLOW FORMATIF F4                     |
+-------------------------------------------------------------+
|                                                             |
|  1. Creer main.py avec la structure de base                 |
|     +-- Imports (time, board, digitalio)                    |
|     +-- Constantes de configuration                         |
|     +-- Fonctions (read_sensor)                             |
|     +-- Garde __main__                                      |
|                                                             |
|  2. Ajouter le pattern timer-in-loop                        |
|     +-- time.monotonic() pour mesurer le temps              |
|     +-- Comparaison d'intervalle (>= SENSOR_INTERVAL)       |
|     +-- Lecture capteur a intervalle regulier                |
|                                                             |
|  3. Ajouter le polling bouton                               |
|     +-- button.value dans la boucle principale              |
|     +-- Detection de transition (appui/relache)             |
|                                                             |
|  4. Ajouter le maintien pour l'arret                        |
|     +-- break quand bouton maintenu >= 2 secondes           |
|     +-- finally pour cleanup (button.deinit())              |
|                                                             |
|  5. Tester sur Raspberry Pi                                 |
|     +-- uv run main.py                                      |
|                                                             |
+-------------------------------------------------------------+
```

---

## Structure de code recommandee

```python
# /// script
# requires-python = ">=3.9"
# dependencies = ["adafruit-blinka"]
# ///
"""Programme principal avec timer et bouton polling."""

import time
import board
import digitalio

# Configuration
SENSOR_INTERVAL = 5  # secondes entre lectures
BUTTON_PIN = board.D17  # GPIO pour le bouton (board.D17 pour Blinka)

# Configuration du bouton
button = digitalio.DigitalInOut(BUTTON_PIN)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP


def read_sensor(sensor):
    """Lire le capteur et afficher les donnees."""
    try:
        temperature = sensor.temperature
        humidity = sensor.relative_humidity
        print(f"Temperature: {temperature:.1f} C, Humidite: {humidity:.1f} %")
    except Exception as e:
        print(f"Erreur lecture: {e}")


def main():
    """Fonction principale avec boucle timer + bouton."""
    import adafruit_ahtx0

    i2c = board.I2C()
    sensor = adafruit_ahtx0.AHTx0(i2c)

    previous_sensor = time.monotonic()
    last_button = True
    press_start = None

    try:
        while True:
            current_time = time.monotonic()

            # Timer: lecture capteur a intervalle regulier
            if current_time - previous_sensor >= SENSOR_INTERVAL:
                read_sensor(sensor)
                previous_sensor = current_time

            # Polling bouton: detection de transition
            current_button = button.value
            if last_button and not current_button:
                print("Bouton appuye!")
            last_button = current_button

            # Maintien bouton: arret apres 2 secondes
            if not current_button:
                if press_start is None:
                    press_start = current_time
                elif current_time - press_start >= 2:
                    print("Arret demande (bouton maintenu)...")
                    break
            else:
                press_start = None

            time.sleep(0.05)
    except KeyboardInterrupt:
        print("Arret demande (Ctrl+C)...")
    finally:
        button.deinit()
        print("Nettoyage termine.")


if __name__ == "__main__":
    main()
```

---

## Points cles

### Pourquoi `time.monotonic()`?

`time.sleep(5)` **bloque** tout le programme pendant 5 secondes -- impossible
de lire le bouton pendant ce temps. `time.monotonic()` mesure le temps ecoule
**sans bloquer**: la boucle continue de tourner rapidement (~50ms) et verifie
si l'intervalle est atteint a chaque iteration.

### Pourquoi le polling dans la boucle principale?

Une seule boucle `while True` gere tout: les timers ET le bouton. A chaque
iteration (~50ms), on verifie si le capteur doit etre lu ET si le bouton est
appuye. C'est le meme pattern que sur un microcontroleur.

### Pourquoi try/except dans la boucle?

Les erreurs de lecture capteur (I2C deconnecte, capteur defaillant) ne doivent
pas faire crasher tout le programme. En entourant le code sensible de
try/except, le programme continue de fonctionner meme si une lecture echoue.

### Pourquoi `break` au lieu de `threading.Event`?

Le pattern timer-in-loop utilise une seule boucle `while True`. Pour en sortir,
on utilise simplement `break` (par exemple, quand le bouton est maintenu pendant
2 secondes). C'est plus simple et direct que le mecanisme Event du threading.
Le threading sera enseigne plus tard dans le cours.

### Pourquoi digitalio polling?

digitalio est la bibliotheque standard CircuitPython pour les GPIO.
Le polling dans la boucle principale est simple, fiable, et fonctionne sur
tous les Raspberry Pi sans dependance supplementaire (via adafruit-blinka).

---

## Livrables

Dans ce depot, vous devez avoir :

- [ ] `main.py` — Script principal avec timer et bouton polling
- [ ] `.test_markers/` — Dossier cree par `validate_pi.py`

---

Bonne chance!
