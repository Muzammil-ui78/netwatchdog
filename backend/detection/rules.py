from collections import defaultdict
from config import Config

port_scan_tracker = defaultdict(set)
syn_flood_tracker = defaultdict(int)
brute_force_tracker = defaultdict(int)
icmp_flood_tracker = defaultdict(int)
udp_flood_tracker = defaultdict(int)
dns_tracker = defaultdict(int)

def check_port_scan(src_ip, dst_port):
    port_scan_tracker[src_ip].add(dst_port)
    if len(port_scan_tracker[src_ip]) >= Config.PORT_SCAN_THRESHOLD:
        port_scan_tracker[src_ip].clear()
        return True
    return False

def check_syn_flood(src_ip):
    syn_flood_tracker[src_ip] += 1
    if syn_flood_tracker[src_ip] >= Config.SYN_FLOOD_THRESHOLD:
        syn_flood_tracker[src_ip] = 0
        return True
    return False

def check_brute_force(src_ip, dst_port):
    if dst_port in [22, 21, 3389, 23, 3306, 5432]:
        brute_force_tracker[src_ip] += 1
        if brute_force_tracker[src_ip] >= Config.BRUTE_FORCE_THRESHOLD:
            brute_force_tracker[src_ip] = 0
            return True
    return False

def check_icmp_flood(src_ip):
    icmp_flood_tracker[src_ip] += 1
    if icmp_flood_tracker[src_ip] >= 50:
        icmp_flood_tracker[src_ip] = 0
        return True
    return False

def check_udp_flood(src_ip):
    udp_flood_tracker[src_ip] += 1
    if udp_flood_tracker[src_ip] >= 200:
        udp_flood_tracker[src_ip] = 0
        return True
    return False

def check_dns_amplification(src_ip, dst_port):
    if dst_port == 53:
        dns_tracker[src_ip] += 1
        if dns_tracker[src_ip] >= 30:
            dns_tracker[src_ip] = 0
            return True
    return False

def check_null_scan(flags):
    return flags == "0" or flags == ""

def check_xmas_scan(flags):
    return "F" in flags and "P" in flags and "U" in flags

def analyze_packet(src_ip, dst_ip, protocol, src_port, dst_port, flags=None, icmp=False):
    threats = []

    if dst_port:
        if check_port_scan(src_ip, dst_port):
            threats.append({
                "type": "PORT_SCAN",
                "severity": "HIGH",
                "src_ip": src_ip,
                "dst_ip": dst_ip,
                "details": f"Port scan detected from {src_ip}"
            })

    if flags and "S" in flags and "A" not in flags:
        if check_syn_flood(src_ip):
            threats.append({
                "type": "SYN_FLOOD",
                "severity": "CRITICAL",
                "src_ip": src_ip,
                "dst_ip": dst_ip,
                "details": f"SYN flood attack from {src_ip}"
            })

    if dst_port:
        if check_brute_force(src_ip, dst_port):
            threats.append({
                "type": "BRUTE_FORCE",
                "severity": "HIGH",
                "src_ip": src_ip,
                "dst_ip": dst_ip,
                "details": f"Brute force attempt from {src_ip} on port {dst_port}"
            })

    if icmp:
        if check_icmp_flood(src_ip):
            threats.append({
                "type": "ICMP_FLOOD",
                "severity": "MEDIUM",
                "src_ip": src_ip,
                "dst_ip": dst_ip,
                "details": f"ICMP flood (ping flood) detected from {src_ip}"
            })

    if protocol == "UDP":
        if check_udp_flood(src_ip):
            threats.append({
                "type": "UDP_FLOOD",
                "severity": "HIGH",
                "src_ip": src_ip,
                "dst_ip": dst_ip,
                "details": f"UDP flood attack detected from {src_ip}"
            })

        if dst_port and check_dns_amplification(src_ip, dst_port):
            threats.append({
                "type": "DNS_AMPLIFICATION",
                "severity": "CRITICAL",
                "src_ip": src_ip,
                "dst_ip": dst_ip,
                "details": f"DNS amplification attack from {src_ip}"
            })

    if flags is not None:
        if check_null_scan(flags):
            threats.append({
                "type": "NULL_SCAN",
                "severity": "MEDIUM",
                "src_ip": src_ip,
                "dst_ip": dst_ip,
                "details": f"Null scan (stealth scan) detected from {src_ip}"
            })

        if check_xmas_scan(flags):
            threats.append({
                "type": "XMAS_SCAN",
                "severity": "HIGH",
                "src_ip": src_ip,
                "dst_ip": dst_ip,
                "details": f"XMAS scan (stealth scan) detected from {src_ip}"
            })

    return threats
