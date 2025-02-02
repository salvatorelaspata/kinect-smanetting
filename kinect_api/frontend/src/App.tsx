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
    // fetchStatus();
  }, []);
  return (
    <main className="p-6 min-h-screen bg-gray-100">
      <KinectControls
        globalStatus={globalStatus}
        error={error}
        setError={setError}
        setGlobalStatus={setGlobalStatus}
      />
      <KinectDualViewer />
    </main>
  );
}

export default App;
