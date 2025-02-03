#!/usr/bin/env python
import freenect
import lib.frame_convert2 as frame_convert2
import cv2
import numpy as np

# Inizializzazione finestre
cv2.namedWindow("Video")
cv2.namedWindow("Depth")

ctx = None
dev = None
tilt_angle = 0


def video_callback(dev, data, timestamp):
    global video_frame
    video_frame = frame_convert2.video_cv(data)


def depth_callback(dev, data, timestamp):
    global depth_frame
    depth_frame = frame_convert2.pretty_depth_cv(data)


def init_kinect():
    global ctx, dev
    ctx = freenect.init()
    dev = freenect.open_device(ctx, 0)

    # Setup callback
    freenect.set_video_callback(dev, video_callback)
    freenect.set_depth_callback(dev, depth_callback)

    # Avvia stream
    freenect.start_video(dev)
    freenect.start_depth(dev)
    return dev


def handle_keys(key):
    global tilt_angle, dev

    # Controllo LED
    if key == ord("q"):
        freenect.set_led(dev, freenect.LED_OFF)
    elif key == ord("e"):
        freenect.set_led(dev, freenect.LED_GREEN)

    # Controllo tilt
    if key == ord("w"):
        tilt_angle = min(30, tilt_angle + 5)
        freenect.set_tilt_degs(dev, tilt_angle)
    elif key == ord("s"):
        tilt_angle = max(-30, tilt_angle - 5)
        freenect.set_tilt_degs(dev, tilt_angle)


try:
    dev = init_kinect()
    print("Premi ESC per uscire")

    while True:
        # Processa eventi Kinect
        freenect.process_events(ctx)

        # Mostra frame se disponibili
        if "video_frame" in globals():
            cv2.imshow("Video", video_frame)
        if "depth_frame" in globals():
            cv2.imshow("Depth", depth_frame)

        # Gestione input
        key = cv2.waitKey(10)
        if key == 27:
            break
        handle_keys(key)

finally:
    # Pulizia
    if dev:
        freenect.stop_video(dev)
        freenect.stop_depth(dev)
        freenect.close_device(dev)
    cv2.destroyAllWindows()
