import React, { useState } from "react";

interface StreamViewProps {
  streamType: "rgb" | "depth";
  width?: number;
  height?: number;
  isSelected?: boolean;
  onSelect?: () => void;
}

const StreamView: React.FC<StreamViewProps> = ({
  streamType,
  width = 640,
  height = 480,
  isSelected = false,
  onSelect,
}) => {
  return (
    <div
      onClick={onSelect}
      className={`
        relative rounded-lg overflow-hidden transition-all duration-300 ease-in-out cursor-pointer 
        ${isSelected ? "scale-100" : "hover:scale-[1.02]"}
        ${isSelected ? "shadow-xl" : "shadow-md hover:shadow-lg"}
      `}
    >
      <div className="absolute top-2 left-2 z-10">
        <span className="px-3 py-1 bg-black/50 text-white rounded-full text-sm">
          {streamType.toUpperCase()}
        </span>
      </div>
      <img
        src={`http://localhost:5003/${
          streamType === "rgb" ? "video" : "depth"
        }`}
        width={width}
        height={height}
        className="w-full h-full object-cover"
        alt={`Kinect ${streamType} stream`}
      />
    </div>
  );
};

const KinectDualViewer: React.FC = () => {
  const [selectedStream, setSelectedStream] = useState<"rgb" | "depth" | null>(
    null
  );

  const handleStreamSelect = (stream: "rgb" | "depth") => {
    setSelectedStream(selectedStream === stream ? null : stream);
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold mb-6 text-gray-800">
          Kinect Stream Viewer
        </h1>

        <div
          className={`
          grid gap-6 transition-all duration-300
          ${
            selectedStream
              ? "grid-cols-1 md:grid-cols-[2fr_1fr]"
              : "grid-cols-1 md:grid-cols-2"
          }
        `}
        >
          {/* RGB Stream */}
          <div
            className={
              selectedStream === "rgb" ? "md:col-span-1 order-first" : ""
            }
          >
            <StreamView
              streamType="rgb"
              isSelected={selectedStream === "rgb"}
              onSelect={() => handleStreamSelect("rgb")}
            />
          </div>

          {/* Depth Stream */}
          <div
            className={
              selectedStream === "depth" ? "md:col-span-1 order-first" : ""
            }
          >
            <StreamView
              streamType="depth"
              isSelected={selectedStream === "depth"}
              onSelect={() => handleStreamSelect("depth")}
            />
          </div>
        </div>

        {/* Instructions */}
        <p className="mt-4 text-center text-gray-600">
          {selectedStream
            ? "Click the selected stream again to return to split view"
            : "Click on either stream to enlarge it"}
        </p>
      </div>
    </div>
  );
};

export default KinectDualViewer;
