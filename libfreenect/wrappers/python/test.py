import freenect
import cv2
import numpy as np


# Funzione per ottenere i dati di profondità
def get_depth():
    depth, _ = freenect.sync_get_depth()
    return depth


# Funzione per ottenere i dati video
def get_video():
    video, _ = freenect.sync_get_video()
    return video


# Ciclo principale
while True:
    depth = get_depth()
    video = get_video()

    # Visualizza i dati di profondità
    cv2.imshow("Depth", depth)

    # Visualizza i dati video
    rgb_frame = cv2.cvtColor(video, cv2.COLOR_RGB2BGR)
    cv2.imshow("Video", rgb_frame)

    # Premi ESC per uscire
    if cv2.waitKey(10) == 27:
        break

# Rilascia le risorse
cv2.destroyAllWindows()
freenect.sync_stop()
