import { Shield, AlertTriangle, Activity, Lock } from "lucide-react";

export default function StatsCards({ stats }) {
  const cards = [
    { label: "Total Packets", value: stats.total_packets, icon: Activity, color: "text-blue-400" },
    { label: "Total Threats", value: stats.total_threats, icon: AlertTriangle, color: "text-red-400" },
    { label: "Port Scans", value: stats.port_scans, icon: Shield, color: "text-amber-400" },
    { label: "Brute Force", value: stats.brute_force, icon: Lock, color: "text-pink-400" },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {cards.map((card, i) => {
        const Icon = card.icon;
        return (
          <div key={i} className="bg-gray-800 border border-gray-700 rounded-lg p-4">
            <div className="flex items-center justify-between mb-2">
              <span className="text-gray-400 text-sm">{card.label}</span>
              <Icon className={`w-5 h-5 ${card.color}`} />
            </div>
            <p className="text-2xl font-semibold text-white">{card.value ?? 0}</p>
          </div>
        );
      })}
    </div>
  );
}