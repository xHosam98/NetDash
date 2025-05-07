import psutil
import datetime
import pandas as pd
import socket

stats_history = []

prev_sent = 0
prev_recv = 0

def is_connected():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except:
        return False

def get_network_stats():
    global prev_sent, prev_recv
    current = psutil.net_io_counters()
    sent = current.bytes_sent
    recv = current.bytes_recv

    upload_speed = (sent - prev_sent) / 1024
    download_speed = (recv - prev_recv) / 1024

    prev_sent = sent
    prev_recv = recv

    return round(upload_speed, 2), round(download_speed, 2)

def get_interface_ip():
    interfaces = psutil.net_if_addrs()
    for iface, addrs in interfaces.items():
        for addr in addrs:
            if addr.family == 2:
                return iface, addr.address
    return "Unknown", "0.0.0.0"

def get_stats():
    upload, download = get_network_stats()
    iface, ip = get_interface_ip()
    return {
        "Time": datetime.datetime.now().strftime("%H:%M:%S"),
        "DateTime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "CPU": psutil.cpu_percent(),
        "RAM": psutil.virtual_memory().percent,
        "Upload": upload,
        "Download": download,
        "Interface": iface,
        "IP": ip,
        "Online": is_connected()
    }

def save_to_csv():
    df = pd.DataFrame(stats_history)
    df.to_csv("system_log.csv", index=False)

def reset_stats():
    global stats_history
    stats_history.clear()
