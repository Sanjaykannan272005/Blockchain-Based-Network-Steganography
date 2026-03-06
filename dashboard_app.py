from flask import Flask, render_template, jsonify
import requests
import time
import threading
import random

app = Flask(__name__)

START_TIME = time.time()

# Load config for RBAC
import json
try:
    with open('blockchain_config.json', 'r') as f:
        config = json.load(f)
        ADMIN_ADDR = config.get('owner_address', config.get('wallet_address', '')).lower()
except:
    ADMIN_ADDR = ""

# Configuration
SERVICES = {
    'auth': 'http://localhost:5002',
    'receiver': 'http://localhost:5001',
    'sender': 'http://localhost:5003'
}

def check_service(url):
    try:
        import requests
        requests.get(url, timeout=1)
        return True
    except:
        return False

@app.route('/')
def index():
    return render_template('dashboard.html', admin_address=ADMIN_ADDR)

@app.route('/api/stats')
def get_stats():
    # 1. Check Service Status
    service_status = {name: check_service(url) for name, url in SERVICES.items()}
    
    # 2. Get Aggregated Metrics (Mocked for Demo purposes)
    import json
    try:
        with open('traffic_profile.json', 'r') as f:
            profile = json.load(f)
        mimicry_score = f"{random.randint(94, 98)}%"
        traffic_dna = f"IAT:{profile['iat_mean']:.3f}s / Size:{int(profile['size_mean'])}B"
    except:
        mimicry_score = "N/A"
        traffic_dna = "Default"

    target_wallet = request.args.get('wallet', '').lower()
    user_role = "GUEST"
    if target_wallet:
        if target_wallet == ADMIN_ADDR.lower():
            user_role = "ADMIN"
        else:
            user_role = "AUTHORIZED" # Simulating authorized for known users in demo app

    metrics = {
        'messages_count': random.randint(5, 50),
        'whitelisted_count': 3,
        'wallet_balance': "0.485",
        'mimicry_score': mimicry_score,
        'traffic_dna': traffic_dna,
        'net_status': 'NORMAL',
        'avg_reputation': 98.2,
        'node_count': 4,
        'current_protocol': 'TIMING',
        'block_number': '1234567',
        'user_role': user_role
    }
    
    # 3. Logs (Simulated)
    logs = []
    if random.random() > 0.7:
        actions = ["New block mined", f"Access verified for {target_wallet[:8]}...", "Protocol sync complete"]
        logs.append(random.choice(actions))

    return jsonify({
        'services': service_status,
        'metrics': metrics,
        'uptime': int(time.time() - START_TIME),
        'logs': logs,
        'chart_data': [random.randint(0, 10) for _ in range(6)]
    })

@app.route('/api/network_map')
def network_map():
    """Return nodes and links for the P2P network map"""
    # In production, this would query active p2p_node instances
    nodes = [
        {"id": "Sender", "role": "entry", "status": "online"},
        {"id": "Relay-1", "role": "relay", "status": "online"},
        {"id": "Relay-2", "role": "relay", "status": "online"},
        {"id": "Recipient", "role": "exit", "status": "online"}
    ]
    links = [
        {"source": "Sender", "target": "Relay-1", "type": "timing"},
        {"source": "Relay-1", "target": "Relay-2", "type": "size"},
        {"source": "Relay-2", "target": "Recipient", "type": "ttl"}
    ]
    return jsonify({"nodes": nodes, "links": links})

if __name__ == '__main__':
    print("🚀 Dashboard Starting on http://localhost:5004")
    app.run(port=5004, debug=True)
