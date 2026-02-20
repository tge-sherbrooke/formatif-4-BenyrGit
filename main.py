# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "adafruit-blinka",
#     "adafruit-circuitpython-ahtx0>=1.0.28",
#     "rpi-gpio>=0.7.1",
# ]
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
