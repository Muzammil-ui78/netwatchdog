import numpy as np
from sklearn.ensemble import IsolationForest
from collections import defaultdict

model = IsolationForest(contamination=0.05, random_state=42)
traffic_data = []
ip_packet_count = defaultdict(int)
ip_port_set = defaultdict(set)
is_trained = False

def extract_features(src_ip, dst_port, protocol, size):
    ip_packet_count[src_ip] += 1
    if dst_port:
        ip_port_set[src_ip].add(dst_port)
    proto_num = 1 if protocol == "TCP" else 2 if protocol == "UDP" else 3
    return [
        ip_packet_count[src_ip],
        len(ip_port_set[src_ip]),
        dst_port if dst_port else 0,
        size,
        proto_num
    ]

def train_model():
    global is_trained
    if len(traffic_data) >= 100:
        model.fit(traffic_data)
        is_trained = True

def detect_anomaly(src_ip, dst_ip, dst_port, protocol, size):
    features = extract_features(src_ip, dst_port, protocol, size)
    traffic_data.append(features)

    if len(traffic_data) % 100 == 0:
        train_model()

    if not is_trained:
        return None

    prediction = model.predict([features])
    score = model.decision_function([features])[0]

    if prediction[0] == -1 and score < -0.2:
        return {
            "type": "ML_ANOMALY",
            "severity": "MEDIUM",
            "src_ip": src_ip,
            "dst_ip": dst_ip,
            "details": f"Anomalous traffic pattern detected from {src_ip} (score: {round(score, 3)})"
        }
    return None
