import freenect
import cv2
import numpy as np


# Funzione per ottenere l'immagine rgb
def get_rgb():
    rgb, _ = freenect.sync_get_video()
    rgb = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    return rgb


# Funzione per ottenere i dati di profondità
def get_depth():
    depth, _ = freenect.sync_get_depth()
    depth = depth.astype(np.uint8)
    depth = cv2.cvtColor(depth, cv2.COLOR_GRAY2BGR)
    return depth


# Funzione per ottenere i dati video
def get_video_rgb():
    # Modifica per ottenere continuamente nuovi frame
    video, _ = freenect.sync_get_video()
    video = cv2.cvtColor(video, cv2.COLOR_RGB2BGR)
    return video


# Funzione per ottenere i dati video depth
def get_video_depth():
    # Modifica per ottenere continuamente nuovi frame
    video, _ = freenect.sync_get_depth()
    video = video.astype(np.uint8)
    # video = cv2.cvtColor(video, cv2.COLOR_GRAY2BGR)
    return video
