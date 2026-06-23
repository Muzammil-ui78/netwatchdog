from datetime import datetime

def create_log(src_ip, dst_ip, protocol, threat_type, severity, details=""):
    return {
        "src_ip": src_ip,
        "dst_ip": dst_ip,
        "protocol": protocol,
        "threat_type": threat_type,
        "severity": severity,
        "details": details,
        "timestamp": datetime.utcnow()
    }

def create_packet_log(src_ip, dst_ip, protocol, src_port, dst_port, size):
    return {
        "src_ip": src_ip,
        "dst_ip": dst_ip,
        "protocol": protocol,
        "src_port": src_port,
        "dst_port": dst_port,
        "size": size,
        "timestamp": datetime.utcnow()
    }