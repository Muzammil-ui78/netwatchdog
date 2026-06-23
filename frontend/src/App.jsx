import { useState, useEffect } from "react";
import { socket } from "./socket";
import StatsCards from "./components/StatsCards";
import ThreatList from "./components/ThreatList";
import { ShieldCheck } from "lucide-react";

function App() {
  const [stats, setStats] = useState({});
  const [threats, setThreats] = useState([]);

  const fetchStats = async () => {
    const res = await fetch("http://127.0.0.1:5000/api/stats");
    const data = await res.json();
    setStats(data);
  };

  const fetchThreats = async () => {
    const res = await fetch("http://127.0.0.1:5000/api/threats");
    const data = await res.json();
    setThreats(data);
  };

  useEffect(() => {
    fetchStats();
    fetchThreats();
    const interval = setInterval(fetchStats, 5000);
    socket.on("new_threat", (threat) => {
      setThreats((prev) => [threat, ...prev].slice(0, 50));
      fetchStats();
    });
    return () => {
      clearInterval(interval);
      socket.off("new_threat");
    };
  }, []);

  return (
    <div className="min-h-screen bg-gray-900 p-6">
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center gap-2 mb-6">
          <ShieldCheck className="w-7 h-7 text-green-400" />
          <h1 className="text-2xl font-semibold text-white">NetWatchdog</h1>
          <span className="text-xs bg-green-500/20 text-green-400 px-2 py-1 rounded-full border border-green-500/30 ml-2">Live</span>
        </div>
        <div className="space-y-6">
          <StatsCards stats={stats} />
          <ThreatList threats={threats} />
        </div>
      </div>
    </div>
  );
}

export default App;
