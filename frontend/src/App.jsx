import { useState, useEffect } from "react";
import StatsCards from "./components/StatsCards";
import ThreatList from "./components/ThreatList";
import { ShieldCheck, WifiOff } from "lucide-react";

function App() {
  const [stats, setStats] = useState({});
  const [threats, setThreats] = useState([]);
  const [online, setOnline] = useState(true);

  const fetchStats = async () => {
    try {
      const res = await fetch("http://127.0.0.1:5000/api/stats");
      const data = await res.json();
      setStats(data);
      setOnline(true);
    } catch {
      setOnline(false);
    }
  };

  const fetchThreats = async () => {
    try {
      const res = await fetch("http://127.0.0.1:5000/api/threats");
      const data = await res.json();
      setThreats(data);
    } catch {
      setOnline(false);
    }
  };

  useEffect(() => {
    fetchStats();
    fetchThreats();
    const interval = setInterval(fetchStats, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gray-900 p-6">
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center gap-2 mb-6">
          <ShieldCheck className="w-7 h-7 text-green-400" />
          <h1 className="text-2xl font-semibold text-white">NetWatchdog</h1>
          <span className={`text-xs px-2 py-1 rounded-full border ml-2 ${online ? "bg-green-500/20 text-green-400 border-green-500/30" : "bg-red-500/20 text-red-400 border-red-500/30"}`}>
            {online ? "Live" : "Offline"}
          </span>
        </div>

        {!online ? (
          <div className="flex flex-col items-center justify-center h-96 gap-4">
            <WifiOff className="w-16 h-16 text-gray-600" />
            <h2 className="text-xl font-medium text-gray-400">Backend Offline</h2>
            <p className="text-gray-500 text-sm text-center max-w-md">
              Run the backend locally to start monitoring your network.
            </p>
            <div className="bg-gray-800 border border-gray-700 rounded-lg p-4 text-sm font-mono text-green-400 mt-2">
              cd backend && python app.py
            </div>
          </div>
        ) : (
          <div className="space-y-6">
            <StatsCards stats={stats} />
            <ThreatList threats={threats} />
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
