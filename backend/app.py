from flask import Flask, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
from pymongo import MongoClient
from config import Config
from sniffer.packet_capture import init_sniffer, start_sniffing
import threading

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

client = MongoClient(Config.MONGO_URI)
db = client[Config.DB_NAME]

init_sniffer(db, socketio)

@app.route("/api/threats", methods=["GET"])
def get_threats():
    threats = list(db.threats.find({}, {"_id": 0}).sort("timestamp", -1).limit(50))
    for t in threats:
        t["timestamp"] = str(t["timestamp"])
    return jsonify(threats)

@app.route("/api/stats", methods=["GET"])
def get_stats():
    return jsonify({
        "total_threats": db.threats.count_documents({}),
        "total_packets": db.packets.count_documents({}),
        "port_scans": db.threats.count_documents({"threat_type": "PORT_SCAN"}),
        "syn_floods": db.threats.count_documents({"threat_type": "SYN_FLOOD"}),
        "brute_force": db.threats.count_documents({"threat_type": "BRUTE_FORCE"})
    })

@app.route("/api/packets", methods=["GET"])
def get_packets():
    packets = list(db.packets.find({}, {"_id": 0}).sort("timestamp", -1).limit(100))
    for p in packets:
        p["timestamp"] = str(p["timestamp"])
    return jsonify(packets)

def start_sniffer_thread():
    thread = threading.Thread(target=start_sniffing, args=(Config.NETWORK_INTERFACE,))
    thread.daemon = True
    thread.start()
@app.route("/api/test-alert", methods=["GET"])
def test_alert():
    from alerts.notifier import notify
    test_threat = {
        "type": "PORT_SCAN",
        "severity": "HIGH",
        "src_ip": "192.168.1.100",
        "dst_ip": "192.168.1.1",
        "details": "Test alert from NetWatchdog"
    }
    notify(test_threat)
    return jsonify({"status": "Test alert sent to Discord!"})
if __name__ == "__main__":
    start_sniffer_thread()
    socketio.run(app, debug=Config.DEBUG, port=5000)