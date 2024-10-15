import time
import board
import neopixel
import keyboard  # Para detectar la presión de teclas

# Configuración de la tira LED
LED_PIN = board.D21 # Pin GPIO que usas
NUM_LEDS = 509       # Número de LEDs en la tira
BRIGHTNESS = 1     # Billo de los LEDs

# Color por defecto
DEFAULT_COLOR = (0, 255, 255)  # Color RGB por defecto

# Límites de las secciones
lim0 = 0
lim1 = 128
lim2 = 256
lim3 = 384
lim4 = 509

strip = neopixel.NeoPixel(LED_PIN, NUM_LEDS, brightness=BRIGHTNESS, auto_write=False)

def turn_off_all_leds():
    """Apagar todos los LEDs."""
    strip.fill((0, 0, 0))
    strip.show()

def turn_on_section(r, g, b, section):
    """Encender la sección correspondiente."""
    start = 0
    end = 0

    if section == 1:
        start, end = lim0, lim1
    elif section == 2:
        start, end = lim1, lim2
    elif section == 3:
        start, end = lim2, lim3
    elif section == 4:
        start, end = lim3, lim4
    else:
        print("Sección no válida. Debe ser un número del 1 al 4.")
        return

    # Encender solo la sección especificada
    for i in range(start, end):
        strip[i] = (r, g, b)
    strip.show()

def blink_color(r, g, b, duration=10, section=2):
    """Función para parpadear un color específico en una sección durante un tiempo determinado."""
    turn_off_all_leds()  # Apagar todos los LEDs antes de comenzar

    end_time = time.time() + duration
    while time.time() < end_time:
        turn_on_section(r, g, b, section)  # Encender la sección
        time.sleep(0.5)  # Encendido por 0.5 segundos

        turn_off_all_leds()  # Apagar los LEDs
        time.sleep(0.5)  # Apagado por 0.5 segundos

    # Restaurar el color por defecto al finalizar
    strip.fill(DEFAULT_COLOR)
    strip.show()

try:
    # Encender el color por defecto al inicio
    strip.fill(DEFAULT_COLOR)
    strip.show()

    print("Presiona 'e' para cambiar el color. Presiona Ctrl+C para salir.")

    while True:
        # Verificar si se presiona la tecla 'e'
        if keyboard.is_pressed('e'):
            print("Tecla 'e' presionada. Cambiando color...")
            # Llama a la función de parpadeo con el color deseado y la sección
            blink_color(255, 0, 0, duration=10, section=1)  # Ejemplo con sección 3

except KeyboardInterrupt:
    # Apagar todos los LEDs al finalizar
    turn_off_all_leds()
    print("Programa terminado.")

except Exception as e:
    print(f"Error: {e}")
    turn_off_all_leds()
