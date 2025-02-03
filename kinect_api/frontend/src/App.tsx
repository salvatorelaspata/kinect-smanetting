import { useEffect, useState } from "react";
import KinectControls from "./components/KinectControls";
import KinectDualViewer from "./components/KinectDualViewer";

export type globalStatusType = "OK" | "ERROR" | "LOADING";
export interface KinectStatus {
  led: globalStatusType;
  status: globalStatusType;
  tilt: globalStatusType;
}

function App() {
  const [globalStatus, setGlobalStatus] = useState<globalStatusType>("LOADING");
  const [status, setStatus] = useState<KinectStatus | null>(null);
  const [error, setError] = useState<string | null>(null);
  const fetchStatus = async () => {
    try {
      const response = await fetch("http://localhost:5003/api/get_status");
      const data = await response.json();
      setStatus(data);
    } catch (err) {
      console.error(err);
      setError("Failed to fetch Kinect status");
    }
  };
  // Fetch initial status
  useEffect(() => {
    (async () => {
      try {
        setError(null);
        setGlobalStatus("LOADING");
        await fetchStatus();
        setGlobalStatus("OK");
      } catch (err) {
        console.error(err);
        setError("Failed to fetch Kinect status");
        setGlobalStatus("ERROR");
      }
    })();
  }, []);
  return (
    <main className="p-6 min-h-screen bg-gray-100">
      {globalStatus === "LOADING" ? (
        <div className="bg-blue-100 border-l-4 border-blue-500 text-blue-700 p-4 mb-4">
          <p className="font-bold">Loading</p>
          <p>Fetching Kinect status...</p>
        </div>
      ) : globalStatus === "OK" ? (
        <>
          <KinectControls
            globalStatus={globalStatus}
            error={error}
            setError={setError}
            setGlobalStatus={setGlobalStatus}
          />
          <KinectDualViewer />
        </>
      ) : (
        <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-4">
          <p className="font-bold">Error</p>
          <p>{error}</p>
        </div>
      )}
    </main>
  );
}

export default App;
