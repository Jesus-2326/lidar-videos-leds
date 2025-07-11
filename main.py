import cv2
import time

video_path = "coca.mp4"
window_name = "VideoKiosko"

# Abrir video
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("Error al abrir el video.")
    exit()

# Obtener FPS original del video
fps = cap.get(cv2.CAP_PROP_FPS)
frame_delay = int(1000 / fps) if fps > 0 else 40  # fallback a 25 fps (~40 ms)

# Crear ventana en pantalla completa
cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    ret, frame = cap.read()

    if not ret:
        # Fin del video: reiniciar desde el principio
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    cv2.imshow(window_name, frame)

    # Espera por frame_delay ms, salir si presionan ESC
    if cv2.waitKey(frame_delay) & 0xFF == 27:
        break

# Cierre limpio
cap.release()
cv2.destroyAllWindows()
