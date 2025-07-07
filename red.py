import serial
import re
import pygame
import cv2
import time
import board
import neopixel

# Configurar puerto serie
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
print("Conectado al puerto serie. Leyendo datos...")

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)

# Lista de videos por zonas (solo zona 1 y 2 activas)
video_files = ["fanta.mp4", "spritee.mp4", "3.mp4", "4.mp4"]
videos = [cv2.VideoCapture(file) for file in video_files]

# Video por defecto
default_video = cv2.VideoCapture("coca.mp4")

# Variables de control
current_video = default_video
video_en_progreso = False
zona_actual = None  # Ninguna zona activa al inicio

# Configuración de la tira LED (una sola zona unificada)
LED_PIN = board.D18
NUM_LEDS = 509
BRIGHTNESS = 1

# Colores por zonas (solo zona 1 y 2 relevantes)
colores_zonas = [
    (165, 255, 0),     # Zona 1: Naranja
    (255, 0, 0),       # Zona 2: Verde
    (0, 0, 0),         # Zonas 3 y 4 ignoradas
    (0, 0, 0)
]

# Color por defecto (blanco completo)
color_por_defecto = (0, 255, 0)

# Inicializar LED strip
strip = neopixel.NeoPixel(LED_PIN, NUM_LEDS, brightness=BRIGHTNESS, auto_write=False)

def turn_off_all_leds():
    strip.fill((0, 0, 0))
    strip.show()

def set_led_color(r, g, b):
    print(f"💡 Encendiendo toda la tira con color ({r}, {g}, {b})")
    strip.fill((r, g, b))
    strip.show()

def restore_default_led_color():
    print("🔁 Restaurando color por defecto (blanco) en toda la tira.")
    strip.fill(color_por_defecto)
    strip.show()

def play_video(video):
    fps = video.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        fps = 30
    ret, frame = video.read()
    if not ret:
        video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        return False

    frame = cv2.resize(frame, (1920, 1080))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pygame_frame = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "RGB")
    screen.blit(pygame_frame, (0, 0))
    pygame.display.flip()
    time.sleep(1 / fps)
    return True

def obtener_datos_sensor():
    if ser.in_waiting > 0:
        data = ser.readline().decode('utf-8').rstrip()
        print(f"📥 Datos recibidos: {data}")
        match = re.search(r'ZONE(\d+)=([A-Z]+)', data)
        if match:
            zona_numerica = int(match.group(1))
            action = match.group(2)
            return zona_numerica, action
    return None, None

# Inicialización al arranque
restore_default_led_color()
current_video = default_video
current_video.set(cv2.CAP_PROP_POS_FRAMES, 0)

# Bucle principal
running = True
while running:
    zona_numerica, action = obtener_datos_sensor()

    if action == "ENTER" and zona_numerica in [1, 2]:
        if zona_actual != zona_numerica:
            zona_actual = zona_numerica

            current_video = videos[zona_numerica - 1]
            current_video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            video_en_progreso = True
            print(f"▶️ Entró a zona {zona_numerica}. Reproduciendo video.")

            color = colores_zonas[zona_numerica - 1]
            turn_off_all_leds()
            set_led_color(*color)

    elif action == "EXIT":
        print(f"🚪 Ignorando EXIT de zona {zona_numerica}.")

    if video_en_progreso:
        if not play_video(current_video):
            video_en_progreso = False
            zona_actual = None
            current_video = default_video
            current_video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            print("✅ Video terminado. Regresando al video por defecto.")
            restore_default_led_color()
    else:
        play_video(current_video)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False

# Salida segura
for video in videos:
    if video:
        video.release()
default_video.release()
cv2.destroyAllWindows()
pygame.quit()
ser.close()
