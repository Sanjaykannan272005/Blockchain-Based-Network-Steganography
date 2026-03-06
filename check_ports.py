import socket
import json

def check_ports():
    ports = [5000, 5001, 5002, 5003]
    results = {}
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            in_use = s.connect_ex(('127.0.0.1', port)) == 0
            results[port] = "In Use" if in_use else "Available"
    
    print(json.dumps(results, indent=4))

if __name__ == "__main__":
    check_ports()
