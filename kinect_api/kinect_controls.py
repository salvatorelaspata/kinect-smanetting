import freenect
from flask import jsonify
import time


def get_tilt_angle():
    """Ottieni l'angolo di inclinazione del Kinect"""
    try:
        dev = freenect.open_device(freenect.init(), 0)
        freenect.update_tilt_state(dev)
        tilt_state = freenect.get_tilt_state(dev)
        tilt_degrees = freenect.get_tilt_degs(tilt_state)

        freenect.close_device(dev)
        return jsonify({"status": "OK", "angle": tilt_degrees})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def set_tilt_angle(angle):
    """Imposta l'angolo di inclinazione del Kinect"""
    try:
        dev = freenect.open_device(freenect.init(), 0)
        if angle < -30 or angle > 30:
            raise ValueError(
                "L'angolo di inclinazione deve essere compreso tra -30 e 30 gradi"
            )

        freenect.set_tilt_degs(dev, float(angle))
        freenect.close_device(dev)
        # close device
        return jsonify({"status": "OK", "angle": angle})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def get_led_state():
    """Ottieni lo stato del LED del Kinect"""
    # this functionality is not available in the current version of libfreenect
    return jsonify({"error": "Not implemented"}), 501
    # try:
    #     dev = freenect.open_device(freenect.init(), 0)
    #     led_state = freenect.get_led(dev)
    #     led_options = {
    #         freenect.LED_OFF: "OFF",
    #         freenect.LED_GREEN: "GREEN",
    #         freenect.LED_RED: "RED",
    #         freenect.LED_YELLOW: "YELLOW",
    #         freenect.LED_BLINK_GREEN: "BLINK_GREEN",
    #         freenect.LED_BLINK_RED_YELLOW: "BLINK_RED_YELLOW",
    #     }
    #     led = led_options.get(led_state, "UNKNOWN")

    #     freenect.close_device(dev)
    #     return jsonify({"status": "OK", "led": led})
    # except Exception as e:
    #     return jsonify({"error": str(e)}), 500


def set_led_state(option):
    """Imposta lo stato del LED del Kinect"""
    options = {
        "OFF": freenect.LED_OFF,
        "GREEN": freenect.LED_GREEN,
        "RED": freenect.LED_RED,
        "YELLOW": freenect.LED_YELLOW,
        "BLINK_GREEN": freenect.LED_BLINK_GREEN,
        "BLINK_RED_YELLOW": freenect.LED_BLINK_RED_YELLOW,
    }
    try:
        dev = freenect.open_device(freenect.init(), 0)
        if option not in options:
            raise ValueError(f"Opzione LED non valida: {option}")

        freenect.set_led(
            dev,
            options.get(option, freenect.LED_OFF),
        )

        # close device
        freenect.close_device(dev)
        return jsonify({"status": "OK", "led": option})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def get_kinect_status():
    """Ottieni lo stato del Kinect,
    per farlo si esegue un test di funzionamento
    dei motori e del LED"""
    try:
        check_tilt_degs = "OK"
        # move from 0 to 30 degrees and to -30 degrees
        try:
            print("START - Testing tilt motor")
            # move to 0 and wait it
            set_tilt_angle(0)
            # await 1 second
            time.sleep(1)

            step = 5
            # move from 0 to 30 degrees
            for angle in range(0, 31, step):
                print(f"ANGLE: {angle}")
                set_tilt_angle(angle)
            # move from 30 to -30 degrees
            for angle in range(30, -31, -step):
                print(f"ANGLE: {angle}")
                set_tilt_angle(angle)
            # move from -30 to 0 degrees
            for angle in range(-30, 1, step):
                print(f"ANGLE: {angle}")
                set_tilt_angle(angle)

            print("END - Testing tilt motor")
        except Exception as e:
            check_tilt_degs = "Errore nell'acquisizione dell'angolo di inclinazione"

        check_led = "OK"
        try:
            print("START - Testing LED")
            for option in [
                "OFF",
                "GREEN",
                "RED",
                "YELLOW",
                "BLINK_GREEN",
                "BLINK_RED_YELLOW",
                "OFF",
            ]:
                print(f"LED: {option}")
                set_led_state(option)
                if option == "BLINK_GREEN" or option == "BLINK_RED_YELLOW":
                    time.sleep(1.5)
                else:
                    time.sleep(1 / 2)
            print("END - Testing LED")
        except Exception as e:
            check_led = "Errore nell'impostazione dell'opzione LED"

        return jsonify(
            {
                "status": "OK",
                "tilt": check_tilt_degs,
                "led": check_led,
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500
