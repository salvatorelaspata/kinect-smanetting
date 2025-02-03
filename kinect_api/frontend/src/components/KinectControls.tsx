import React, { useEffect, useState } from "react";
import { Sliders, Power } from "lucide-react";
import { globalStatusType } from "../App";
// import { KinectStatus } from "../App";

interface KinectControlsProps {
  globalStatus: globalStatusType;
  error: string | null;
  setError: (error: string) => void;
  setGlobalStatus: (status: globalStatusType) => void;
}

const KinectControls: React.FC<KinectControlsProps> = ({
  globalStatus,
  error,
  setError,
  setGlobalStatus,
}) => {
  const [tiltAngle, setTiltAngle] = useState<number>(0);
  const [isLoading, setIsLoading] = useState(false);
  const [led_state, setLedState] = useState<string | null>(null);
  // LED options based on the Kinect API
  const ledOptions = [
    { value: "OFF", label: "Off" },
    { value: "GREEN", label: "Green" },
    { value: "RED", label: "Red" },
    { value: "YELLOW", label: "Yellow" },
    { value: "BLINK_GREEN", label: "Blink Green" },
    { value: "BLINK_RED_YELLOW", label: "Blink Red-Yellow" },
  ];

  const handleTiltChange = async (angle: number) => {
    const newAngle = angle;
    if (newAngle === tiltAngle) return;
    await applyTilt();
    setTiltAngle(newAngle);
  };

  const applyTilt = async () => {
    setIsLoading(true);
    try {
      const response = await fetch(`http://localhost:5003/tilt`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
        },
        body: JSON.stringify({ angle: tiltAngle }),
      });

      if (!response.ok) throw new Error("Failed to set tilt angle");

      // await fetchStatus(); // Refresh status after change
    } catch (err) {
      console.error(err);
      setError("Failed to set tilt angle");
      setGlobalStatus("ERROR");
    } finally {
      setIsLoading(false);
    }
  };

  const handleLEDChange = async (
    event: React.ChangeEvent<HTMLSelectElement>
  ) => {
    setIsLoading(true);
    try {
      const response = await fetch(
        `http://localhost:5003/led/${event.target.value}`,
        {
          method: "POST",
        }
      );

      if (!response.ok) throw new Error("Failed to set LED state");

      setLedState(event.target.value);
      // await fetchStatus(); // Refresh status after change
    } catch (err) {
      console.error(err);
      setError("Failed to set LED state");
      setGlobalStatus("ERROR");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const response = await fetch("http://localhost:5003/status");
        const data = await response.json();
        setTiltAngle(data.tilt_angle);
        setGlobalStatus(data.connected ? "OK" : "DISCONNECTED");
      } catch (err) {
        setGlobalStatus("ERROR");
      }
    };
    fetchStatus();
    // const interval = setInterval(fetchStatus, 10000);
    // return () => clearInterval(interval);
  }, [setGlobalStatus]);

  if (isLoading) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-md mb-4">
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold flex items-center gap-2">
              <Sliders className="w-5 h-5" />
              Kinect Controls
            </h2>
            <span className="px-3 py-1 rounded-full text-sm bg-blue-100 text-blue-800">
              Loading...
            </span>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-md mb-4">
      <div className="space-y-6">
        {/* Title */}
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-semibold flex items-center gap-2">
            <Sliders className="w-5 h-5" />
            Kinect Controls
          </h2>
          <span
            className={`px-3 py-1 rounded-full text-sm ${
              globalStatus === "OK"
                ? "bg-green-100 text-green-800"
                : "bg-red-100 text-red-800"
            }`}
          >
            {globalStatus || "Disconnected"}
          </span>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 text-red-600 p-3 rounded-md text-sm">
            {error}
          </div>
        )}

        {/* Tilt Control */}
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-700">
            Tilt Angle ({tiltAngle}°)
          </label>
          <div className="flex gap-2">
            {/* create -30, -20 ... 20, 30 */}
            {Array.from({ length: 13 }, (_, i) => i - 6).map((angle) => (
              <button
                key={angle * 5}
                onClick={() => handleTiltChange(angle * 5)}
                className={`px-3 py-2 rounded-md border ${
                  tiltAngle === angle * 5
                    ? "bg-blue-500 text-white"
                    : "bg-white text-gray-700"
                }`}
              >
                {angle * 5}
              </button>
            ))}
          </div>
        </div>

        {/* LED Control */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-gray-700 flex items-center gap-2">
            <Power className="w-4 h-4" />
            LED State
          </label>
          <select
            value={led_state || ""}
            onChange={handleLEDChange}
            disabled={isLoading}
            className="w-full p-2 border rounded-md bg-white"
          >
            {ledOptions.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
      </div>
    </div>
  );
};

export default KinectControls;
