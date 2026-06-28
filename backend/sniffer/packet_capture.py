from scapy.all import sniff, IP, TCP, UDP, ICMP
from detection.rules import analyze_packet
from detection.ml_detector import detect_anomaly
from models.log_model import create_log, create_packet_log
from alerts.notifier import notify
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

db = None
socketio = None

def init_sniffer(database, socket):
    global db, socketio
    db = database
    socketio = socket

def process_packet(packet):
    try:
        if not packet.haslayer(IP):
            return

        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        protocol = "TCP" if packet.haslayer(TCP) else "UDP" if packet.haslayer(UDP) else "ICMP" if packet.haslayer(ICMP) else "OTHER"
        src_port = None
        dst_port = None
        flags = None
        icmp = False

        if packet.haslayer(TCP):
            src_port = packet[TCP].sport
            dst_port = packet[TCP].dport
            flags = str(packet[TCP].flags)
        elif packet.haslayer(UDP):
            src_port = packet[UDP].sport
            dst_port = packet[UDP].dport
        elif packet.haslayer(ICMP):
            icmp = True

        size = len(packet)

        if db is not None:
            db.packets.insert_one(create_packet_log(src_ip, dst_ip, protocol, src_port, dst_port, size))

        threats = analyze_packet(src_ip, dst_ip, protocol, src_port, dst_port, flags, icmp)

        ml_threat = detect_anomaly(src_ip, dst_ip, dst_port, protocol, size)
        if ml_threat:
            threats.append(ml_threat)

        for threat in threats:
            log = create_log(
                src_ip=threat["src_ip"],
                dst_ip=threat["dst_ip"],
                protocol=protocol,
                threat_type=threat["type"],
                severity=threat["severity"],
                details=threat["details"]
            )
            if db is not None:
                db.threats.insert_one(log)
            if socketio is not None:
                socketio.emit("new_threat", {
                    "type": threat["type"],
                    "severity": threat["severity"],
                    "src_ip": threat["src_ip"],
                    "dst_ip": threat["dst_ip"],
                    "details": threat["details"]
                })
            notify(threat)

    except Exception as e:
        print(f"Packet processing error: {e}")

def start_sniffing(interface=None):
    print(f"Starting packet capture on interface: {interface or 'default'}")
    sniff(iface=interface, prn=process_packet, store=False)
