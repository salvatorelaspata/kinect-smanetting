from flask import Flask, jsonify, Response

import api
import cv2

app = Flask(__name__)


# Rotta che restituisce l'immagine depth
@app.route("/depth")
def demo():
    depth = api.get_depth()
    return cv2.imencode(".png", depth)[1].tobytes(), 200, {"Content-Type": "image/png"}


# Rotta che restituisce l'immagine rgb
@app.route("/rgb")
def rgb():
    rgb = api.get_rgb()
    return cv2.imencode(".png", rgb)[1].tobytes(), 200, {"Content-Type": "image/png"}


# Rotta che restituisce uno streaming video
@app.route("/video-rgb")
def video_rgb():
    return Response(
        generate_video_frames("rgb"),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


@app.route("/video-depth")
def video_depth():
    return Response(
        generate_video_frames("depth"),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


def generate_video_frames(type):
    print("Generating video frames")
    print(type)
    while True:
        if type == "rgb":
            frame = api.get_video_rgb()
        if type == "depth":
            frame = api.get_video_depth()
        else:
            break
        # Converti il frame in JPEG invece di PNG per performance
        ret, buffer = cv2.imencode(".jpg", frame)
        frame_bytes = buffer.tobytes()
        yield (
            b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
        )


@app.route("/health")
def health():
    return jsonify({"status": "OK"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
