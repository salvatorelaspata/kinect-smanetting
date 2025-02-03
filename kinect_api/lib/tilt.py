#!/usr/bin/env python
import freenect
import lib.frame_convert2 as frame_convert2
import cv2

# Inizializzazione finestre
cv2.namedWindow("Video")
cv2.moveWindow("Video", 0, 0)
cv2.namedWindow("Depth")
cv2.moveWindow("Depth", 640, 0)

# Inizializzazione Kinect
ctx = freenect.init()
dev = freenect.open_device(ctx, 0)


# Callback per i frame
def video_callback(dev, data, timestamp):
    cv2.imshow("Video", frame_convert2.video_cv(data))


def depth_callback(dev, data, timestamp):
    cv2.imshow("Depth", frame_convert2.pretty_depth_cv(data))


# Registrazione callback corretta
freenect.set_video_callback(dev, video_callback)
freenect.set_depth_callback(dev, depth_callback)

# Avvio stream (senza parametri aggiuntivi)
# freenect.start_video(dev)
# freenect.start_depth(dev)


def controls(key):
    if key == 27:  # ESC
        freenect.stop_video(dev)
        freenect.stop_depth(dev)
        freenect.close_device(dev)
        cv2.destroyAllWindows()
        exit()
    elif key == 119:
        freenect.set_tilt_degs(dev, 30)  # W
    elif key == 115:
        freenect.set_tilt_degs(dev, -30)  # S
    elif key == 113:
        freenect.set_led(dev, 0)  # Q
    elif key == 101:
        freenect.set_led(dev, 1)  # E
    elif key == 114:
        freenect.set_led(dev, 2)  # R
    elif key == 121:
        freenect.set_led(dev, 3)  # Y
    elif key == 103:
        freenect.set_led(dev, 4)  # G
    elif key == 116:
        freenect.set_led(dev, 6)  # T


# Loop principale corretto
while True:
    freenect.process_events(ctx)
    controls(cv2.waitKey(10))
