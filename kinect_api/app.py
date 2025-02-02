from flask import Flask, jsonify, Response, request, Blueprint
from flask_cors import CORS

import api.api as api
from api.kinect_controls import (
    set_tilt_angle,
    set_led_state,
    get_kinect_status,
    get_tilt_angle,
    get_led_state,
)
import cv2
import numpy as np
import open3d as o3d
from io import BytesIO
from flask import send_file
import tempfile

app = Flask(__name__)
CORS(app)  # Abilita CORS per tutte le rotte


@app.route("/")
def hello():
    # create link to all routes
    return """
    <h1>API Kinect</h1>
    <ul>
        <li><a href="/api/depth">[IMAGE] Depth</a></li>
        <li><a href="/api/rgb">[IMAGE] RGB</a></li>
        <li><a href="/api/video/depth">[VIDEO] Depth</a></li>
        <li><a href="/api/video/rgb">[VIDEO] RGB</a></li>
        <li><a href="/api/health">[GET] Health</a></li>
        <li><a href="/api/raw_depth">[GET] Raw Depth</a></li>
        <li><a href="/api/raw_depth_image">[IMAGE] Raw Depth</a></li>
        <li><a href="/api/depth_meters">[GET] Depth in meters</a></li>
        <li><a href="/api/download_ply">[GET] Download PLY</a></li>
        <li><a href="/api/set_tilt">[POST] Set tilt</a></li>
        <li><a href="/api/set_led">[POST] Set LED</a></li>
        <li><a href="/api/get_status">[GET] Get status</a></li>
    </ul>
    """


api_blueprint = Blueprint("api", __name__)


# Rotta che restituisce l'immagine rgb
@api_blueprint.route("/rgb")
def rgb():
    rgb = api.get_rgb()
    return cv2.imencode(".png", rgb)[1].tobytes(), 200, {"Content-Type": "image/png"}


# Rotta che restituisce l'immagine depth
@api_blueprint.route("/depth")
def demo():
    depth = api.get_depth()
    return cv2.imencode(".png", depth)[1].tobytes(), 200, {"Content-Type": "image/png"}


# Rotta che restituisce uno streaming video
@api_blueprint.route("/video/rgb")
def video_rgb():
    return Response(
        generate_video_frames("rgb"),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


@api_blueprint.route("/video/depth")
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
        elif type == "depth":
            frame = api.get_video_depth()
        else:
            break
        # Converti il frame in JPEG invece di PNG per performance
        ret, buffer = cv2.imencode(".jpg", frame)
        frame_bytes = buffer.tobytes()
        yield (
            b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
        )


@api_blueprint.route("/health")
def health():
    return jsonify({"status": "OK"})


@api_blueprint.route("/raw_depth")
def raw_depth():
    depth = api.get_raw_depth()
    return jsonify({"depth_array": depth.tolist(), "shape": depth.shape})


@api_blueprint.route("/raw_depth_image")
def raw_depth_image():
    depth_raw = api.get_raw_depth()
    # Normalizza a 0-255 e converti in uint8
    depth_normalized = cv2.normalize(
        depth_raw, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U
    )
    _, buffer = cv2.imencode(".png", depth_normalized)
    return Response(buffer.tobytes(), mimetype="image/png")


@api_blueprint.route("/depth_meters")
def depth_meters():
    depth_data = api.get_depth_in_meters()
    return jsonify(
        {
            "depth_array_sample": depth_data[
                :5, :5
            ].tolist(),  # Esempio di una porzione 5x5
            "min_distance": np.min(depth_data),
            "max_distance": np.max(depth_data),
            "shape": depth_data.shape,
        }
    )


def generate_ply():
    depth_data = api.get_raw_depth()
    if depth_data is None:
        return None

    # Converti a metri e genera punti 3D
    depth_meters = 1.0 / (depth_data * -0.0030711016 + 3.3309495161)
    fx, fy, cx, cy = 525, 525, 319.5, 239.5  # Sostituisci con valori calibrati

    u, v = np.meshgrid(np.arange(640), np.arange(480))
    Z = depth_meters
    X = (u - cx) * Z / fx
    Y = (v - cy) * Z / fy

    mask = (Z > 0.3) & (Z < 4.0)  # Filtra rumore e outliers
    points = np.stack([X[mask], Y[mask], Z[mask]], axis=-1)

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)

    # Salva in un file temporaneo
    with tempfile.NamedTemporaryFile(suffix=".ply") as tmp:
        o3d.io.write_point_cloud(tmp.name, pcd)
        tmp.seek(0)
        ply_data = tmp.read()

    return ply_data


@api_blueprint.route("/download_ply")
def download_ply():
    ply_data = generate_ply()
    if ply_data is None:
        return jsonify({"error": "Acquisizione fallita"}), 500

    return Response(
        ply_data,
        mimetype="application/octet-stream",
        headers={"Content-Disposition": "attachment;filename=scan.ply"},
    )


# kinect_controls.py
@api_blueprint.route("/get_tilt_angle")
def handle_get_tilt_angle():
    return get_tilt_angle()


@api_blueprint.route("/set_tilt", methods=["POST"])
def handle_set_tilt():
    angle = request.json.get("angle")
    return set_tilt_angle(angle)


@api_blueprint.route("/get_led_state")
def handle_get_led_state():
    return get_led_state()


@api_blueprint.route("/set_led", methods=["POST"])
def handle_set_led():
    option = request.json.get("option")
    return set_led_state(option)


@api_blueprint.route("/get_status")
def handle_get_status():
    return get_kinect_status()


app.register_blueprint(api_blueprint, url_prefix="/api")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
