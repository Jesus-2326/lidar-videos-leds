import time
import board
import neopixel

# Configuración de la tira LED
LED_PIN = board.D21  # Cambia según el pin que uses
NUM_LEDS = 150        # Número de LEDs en la tira
BRIGHTNESS = 0.5      # Brillo de los LEDs

strip = neopixel.NeoPixel(LED_PIN, NUM_LEDS, brightness=BRIGHTNESS, auto_write=False)

# Animación simple para probar los LEDs
def color_wipe(color, wait_ms=50):
    for i in range(NUM_LEDS):
        strip[i] = color
        strip.show()
        time.sleep(wait_ms / 1000.0)

try:
    while True:
        print("Encendiendo en rojo")
        color_wipe((255, 0, 0))  # Rojo
        time.sleep(1)
        print("Encendiendo en verde")
        color_wipe((0, 255, 0))  # Verde
        time.sleep(1)
        print("Encendiendo en azul")
        color_wipe((0, 0, 255))  # Azul
        time.sleep(1)

except KeyboardInterrupt:
    # Apagar todos los LEDs al finalizar
    strip.fill((0, 0, 0))
    strip.show()
