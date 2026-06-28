import { AlertCircle } from "lucide-react";

const severityColor = {
  CRITICAL: "bg-red-500/20 text-red-400 border-red-500/30",
  HIGH: "bg-amber-500/20 text-amber-400 border-amber-500/30",
  MEDIUM: "bg-blue-500/20 text-blue-400 border-blue-500/30",
  LOW: "bg-green-500/20 text-green-400 border-green-500/30",
};

const typeIcon = {
  PORT_SCAN: "??",
  SYN_FLOOD: "??",
  BRUTE_FORCE: "??",
  ICMP_FLOOD: "??",
  UDP_FLOOD: "??",
  DNS_AMPLIFICATION: "??",
  NULL_SCAN: "??",
  XMAS_SCAN: "??",
  ML_ANOMALY: "??",
};

export default function ThreatList({ threats }) {
  return (
    <div className="bg-gray-800 border border-gray-700 rounded-lg p-4">
      <h2 className="text-white font-medium mb-4 flex items-center gap-2">
        <AlertCircle className="w-5 h-5 text-red-400" />
        Live Threat Feed
      </h2>

      {threats.length === 0 ? (
        <p className="text-gray-500 text-sm">No threats detected yet.</p>
      ) : (
        <div className="space-y-2 max-h-96 overflow-y-auto">
          {threats.map((threat, i) => {
            const threatType = threat.type || threat.threat_type || "UNKNOWN";
            return (
              <div key={i} className={`border rounded-md p-3 ${severityColor[threat.severity] || "bg-gray-700 text-gray-300 border-gray-600"}`}>
                <div className="flex justify-between items-start">
                  <span className="font-medium text-sm">
                    {typeIcon[threatType] || "??"} {threatType}
                  </span>
                  <span className="text-xs opacity-70">{threat.severity}</span>
                </div>
                <p className="text-xs mt-1 opacity-80">{threat.details}</p>
                <p className="text-xs mt-1 opacity-60">From: {threat.src_ip}</p>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
