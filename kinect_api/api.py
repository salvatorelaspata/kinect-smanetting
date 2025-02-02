import freenect
import cv2
import numpy as np


def get_depth_in_meters():
    try:
        depth_data = freenect.sync_get_depth(format=freenect.DEPTH_11BIT)
        if depth_data is None:
            raise ValueError("Kinect non rilevato o dati non disponibili")
        depth_raw = depth_data[0]
        depth_meters = 1.0 / (depth_raw * -0.0030711016 + 3.3309495161)
        return depth_meters
    except Exception as e:
        print(f"Errore nell'acquisizione depth: {e}")
        return None


def get_raw_depth():
    depth, _ = freenect.sync_get_depth(format=freenect.DEPTH_11BIT)
    return depth  # Array numpy a 16-bit (valori 0-2047)


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
    # colora i pixel in base alla profondità (dal rosso al blu)
    video = cv2.applyColorMap(video, cv2.COLORMAP_JET)
    return video
