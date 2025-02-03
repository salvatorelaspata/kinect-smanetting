#!/usr/bin/env python
from flask import Flask, Response, jsonify, request
from flask_cors import CORS
import threading
import freenect
import lib.frame_convert2 as frame_convert2
import cv2
import time

app = Flask(__name__)
CORS(app)


class KinectDevice:
    def __init__(self):
        self.ctx = None
        self.dev = None
        self.tilt_angle = 0
        self.running = False
        self.video_frame = None
        self.depth_frame = None
        self.lock = threading.Lock()

    def init_kinect(self):
        try:
            self.ctx = freenect.init()
            self.dev = freenect.open_device(self.ctx, 0)

            freenect.set_video_callback(self.dev, self.video_callback)
            freenect.set_depth_callback(self.dev, self.depth_callback)
            # freenect.set_video_mode(self.dev, freenect.VIDEO_RGB)
            # freenect.set_depth_mode(self.dev, freenect.DEPTH_11BIT)

            freenect.start_video(self.dev)
            freenect.start_depth(self.dev)
            self.running = True
            return True
        except Exception as e:
            print(f"Init error: {str(e)}")
            return False

    def video_callback(self, dev, data, timestamp):
        with self.lock:
            self.video_frame = frame_convert2.video_cv(data)

    def depth_callback(self, dev, data, timestamp):
        with self.lock:
            self.depth_frame = frame_convert2.pretty_depth_cv(data)

    def process_events(self):
        while self.running:
            freenect.process_events(self.ctx)
            time.sleep(0.01)

    def shutdown(self):
        self.running = False
        if self.dev:
            freenect.stop_video(self.dev)
            freenect.stop_depth(self.dev)
            freenect.close_device(self.dev)
        if self.ctx:
            freenect.shutdown(self.ctx)


kinect = KinectDevice()


# Endpoint API
@app.route("/video")
def video_stream():
    def generate():
        while True:
            with kinect.lock:
                if kinect.video_frame is not None:
                    ret, jpeg = cv2.imencode(".jpg", kinect.video_frame)
                    yield (
                        b"--frame\r\n"
                        b"Content-Type: image/jpeg\r\n\r\n"
                        + jpeg.tobytes()
                        + b"\r\n\r\n"
                    )
                time.sleep(0.03)

    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/depth")
def depth_stream():
    def generate():
        while True:
            with kinect.lock:
                if kinect.depth_frame is not None:
                    ret, jpeg = cv2.imencode(".jpg", kinect.depth_frame)
                    yield (
                        b"--frame\r\n"
                        b"Content-Type: image/jpeg\r\n\r\n"
                        + jpeg.tobytes()
                        + b"\r\n\r\n"
                    )
                time.sleep(0.03)

    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/led/<state>", methods=["POST"])
def set_led(state):
    states = {
        "OFF": freenect.LED_OFF,
        "GREEN": freenect.LED_GREEN,
        "RED": freenect.LED_RED,
        "YELLOW": freenect.LED_YELLOW,
        "BLINK_GREEN": freenect.LED_BLINK_GREEN,
        "BLINK_RED_YELLOW": freenect.LED_BLINK_RED_YELLOW,
    }
    if state in states and kinect.dev:
        freenect.set_led(kinect.dev, states[state])
        return jsonify(status="success")
    return jsonify(status="invalid command"), 400


# Rotta che permette di settare l'angolo di inclinazione del Kinect
# riceve nel body un json con il campo "angle" che rappresenta l'angolo di inclinazione
@app.route("/tilt", methods=["POST"])
def set_tilt():
    body = request.json
    angle = body.get("angle")
    if kinect.dev and -30 <= angle <= 30:
        freenect.set_tilt_degs(kinect.dev, angle)
        kinect.tilt_angle = angle
        return jsonify(status="success", angle=angle)
    return jsonify(status="invalid angle"), 400


@app.route("/status")
def get_status():
    return jsonify(
        connected=kinect.dev is not None,
        tilt_angle=kinect.tilt_angle,
        resolution="640x480",
    )


if __name__ == "__main__":
    if kinect.init_kinect():
        try:
            thread = threading.Thread(target=kinect.process_events)
            thread.start()
            app.run(
                host="0.0.0.0",
                port=5003,
                threaded=True,
                use_reloader=False,  # Importante per evitare doppia inizializzazione
                use_debugger=False,  # Necessario per il corretto funzionamento dello streaming
            )
        finally:
            kinect.shutdown()
    else:
        print("Failed to initialize Kinect")
