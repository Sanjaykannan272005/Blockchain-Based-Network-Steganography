"""
Refactors dashboard.html and sender_web.html:
1. Removes "Covert Transmission Control" block (lines 208-443) from dashboard.html
2. Replaces mock metric elements with live data fields
3. Rewrites sender_web.html with full sending capability (Network Stego, Blockchain Drop, P2P)
"""
import re

# =============================================
# Step 1: Patch dashboard.html
# =============================================
with open('templates/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# --- Remove Transmission Control block ---
# Find from the comment that opens it to the closing pair of div tags (</div></div></div>)
start_marker = '        <!-- NEW: Transmission Control Center -->'
end_marker_after = '        <!-- Charts & Map Row -->'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker_after)

if start_idx == -1 or end_idx == -1:
    print(f"ERROR: Could not find markers. Start found: {start_idx != -1}, End found: {end_idx != -1}")
    print("Searching for alternative markers...")
    # Print context around search area
    idx = content.find('Transmission Control')
    if idx > -1:
        print(f"Found 'Transmission Control' at char {idx}")
        print(repr(content[idx-100:idx+200]))
else:
    # Keep everything before the block and from end_idx onward
    new_analytics_block = """        <!-- Live Blockchain Analytics Row -->
        <div class="row mb-4">
            <div class="col-md-3">
                <div class="card p-4 text-center">
                    <div id="metric-balance" class="metric-value text-success" style="font-size: 1.5rem;">---</div>
                    <div class="metric-label">💰 Wallet Balance (ETH)</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card p-4 text-center">
                    <div id="metric-protocol" class="metric-value text-primary" style="font-size: 1.4rem;">---</div>
                    <div class="metric-label">📡 Active Protocol</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card p-4 text-center">
                    <div id="metric-nodes" class="metric-value text-info" style="font-size: 1.5rem;">---</div>
                    <div class="metric-label">🕸️ Registered Nodes</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card p-4 text-center">
                    <div id="metric-reputation" class="metric-value text-warning" style="font-size: 1.5rem;">---</div>
                    <div class="metric-label">⚖️ Avg. Reputation</div>
                </div>
            </div>
        </div>

        <!-- Security Center + Sender CTA Row -->
        <div class="row mb-4">
            <div class="col-md-8">
                <div class="card p-4 bg-dark text-white h-100">
                    <h5 class="mb-3"><i class="fas fa-shield-alt text-primary me-2"></i>Security Center (C2)</h5>
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label class="form-label small fw-bold text-light">Blockchain Whitelist</label>
                            <div class="input-group input-group-sm">
                                <input type="text" id="whitelistWallet" class="form-control" placeholder="Sender Wallet 0x...">
                                <button class="btn btn-outline-primary" onclick="authorizeSender()">Authorize</button>
                            </div>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label small fw-bold text-light">Global Protocol Switch</label>
                            <div class="d-flex gap-2">
                                <button class="btn btn-sm btn-outline-info flex-grow-1" onclick="switchProtocol('timing')">⏱️ Timing</button>
                                <button class="btn btn-sm btn-outline-info flex-grow-1" onclick="switchProtocol('size')">📦 Size</button>
                                <button class="btn btn-sm btn-outline-info flex-grow-1" onclick="switchProtocol('ttl')">⏳ TTL</button>
                            </div>
                        </div>
                    </div>
                    <hr class="border-secondary">
                    <div class="d-flex align-items-center justify-content-between">
                        <div>
                            <div class="small text-muted">Identity Registry</div>
                            <div class="small">Organization: <span id="reg-org" class="fw-bold text-light">---</span></div>
                            <div class="small">Clearance: <span id="reg-clearance" class="badge bg-secondary">---</span></div>
                        </div>
                        <button class="btn btn-sm btn-primary" onclick="checkClearance()">Refresh Identity</button>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card p-4 text-center h-100 border-success border-2 d-flex flex-column justify-content-center">
                    <div class="fs-1 mb-2">📤</div>
                    <h5 class="fw-bold mb-2">Covert Transmitter</h5>
                    <p class="text-muted small">Send encrypted messages via Network Steganography, P2P Onion Routing, or Blockchain Dead Drop.</p>
                    <a href="http://localhost:5003" target="_blank" class="btn btn-success btn-lg mt-2">
                        <i class="fas fa-paper-plane me-2"></i>Open Sender
                    </a>
                </div>
            </div>
        </div>

        """

    content = content[:start_idx] + new_analytics_block + content[end_idx:]
    print("✅ Removed Transmission Control block and added analytics section")
    print(f"  Block removed: chars {start_idx} to {end_idx}")

# --- Update JS in dashboard to handle new metric fields ---
old_js_metrics = "document.getElementById('metric-messages').textContent = data.metrics.messages_count;"
new_js_metrics = """document.getElementById('metric-messages').textContent = data.metrics.messages_count || 0;
            if(document.getElementById('metric-balance')) document.getElementById('metric-balance').textContent = data.metrics.wallet_balance || '---';
            if(document.getElementById('metric-protocol')) document.getElementById('metric-protocol').textContent = data.metrics.current_protocol || '---';
            if(document.getElementById('metric-nodes')) document.getElementById('metric-nodes').textContent = data.metrics.node_count !== undefined ? data.metrics.node_count : '---';
            if(document.getElementById('metric-reputation')) document.getElementById('metric-reputation').textContent = data.metrics.avg_reputation || '---';"""

if old_js_metrics in content:
    content = content.replace(old_js_metrics, new_js_metrics)
    print("✅ Updated JS metrics update code")
else:
    print("⚠️  Could not find JS metrics update code - may need manual update")

# Fix the old back link in sender_web.html pointing to 5004
with open('templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ Saved dashboard.html")

# =============================================
# Step 2: Rewrite sender_web.html with ALL send capabilities
# =============================================
sender_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Covert Transmitter - Steganography Network</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        body { background: linear-gradient(135deg, #0a0a1a 0%, #111827 100%); color: #e5e7eb; font-family: \'Inter\', sans-serif; min-height: 100vh; }
        .page-header { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 60%, #0d1b3e 100%); padding: 24px 30px; margin-bottom: 30px; box-shadow: 0 4px 20px rgba(0,0,0,0.4); }
        .card { background: #1f2937; border: 1px solid #374151; border-radius: 14px; box-shadow: 0 4px 20px rgba(0,0,0,0.3); margin-bottom: 20px; }
        .card:hover { border-color: #4b5563; box-shadow: 0 6px 30px rgba(59,130,246,0.15); }
        .nav-pills .nav-link { color: #9ca3af; border: 1px solid #374151; margin-right: 6px; border-radius: 8px; font-weight: 500; }
        .nav-pills .nav-link.active { background: linear-gradient(135deg, #1e3c72, #2a5298); border-color: #2a5298; color: white; }
        .form-control, .form-select { background: #111827; border: 1px solid #374151; color: #e5e7eb; border-radius: 8px; }
        .form-control:focus, .form-select:focus { background: #111827; border-color: #3b82f6; color: #e5e7eb; box-shadow: 0 0 0 3px rgba(59,130,246,0.2); }
        .form-control::placeholder { color: #6b7280; }
        .btn-transmit { background: linear-gradient(135deg, #10b981, #059669); border: none; color: white; font-weight: 700; border-radius: 10px; padding: 12px 30px; font-size: 1rem; transition: all 0.2s; }
        .btn-transmit:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(16,185,129,0.4); color: white; }
        .btn-blockchain { background: linear-gradient(135deg, #f59e0b, #d97706); border: none; color: white; font-weight: 700; border-radius: 10px; padding: 12px 30px; }
        .btn-blockchain:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(245,158,11,0.4); color: white; }
        .stat-card { background: #111827; border: 1px solid #374151; border-radius: 10px; padding: 14px; text-align: center; }
        .stat-value { font-size: 1.6rem; font-weight: 700; }
        .stat-label { font-size: 0.72rem; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 2px; }
        .section-title { font-weight: 600; font-size: 1.1rem; color: #e5e7eb; margin-bottom: 18px; display: flex; align-items: center; gap: 10px; }
        .result-box { border-radius: 10px; padding: 16px; margin-top: 16px; font-family: monospace; font-size: 0.85rem; background: #111827; border: 1px solid #374151; display: none; }
        .result-box.success { border-color: #10b981; background: rgba(16,185,129,0.1); }
        .result-box.error { border-color: #ef4444; background: rgba(239,68,68,0.1); }
        .field-label { font-size: 0.82rem; font-weight: 600; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px; }
        .hop-item { background: #111827; border: 1px solid #374151; border-radius: 8px; padding: 12px; margin-bottom: 10px; position: relative; }
        .hop-item .remove-hop { position: absolute; top: 8px; right: 8px; cursor: pointer; color: #ef4444; font-size: 0.8rem; }
        a.back-btn { background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.3); color: white; border-radius: 8px; padding: 6px 16px; text-decoration: none; font-size: 0.85rem; }
        a.back-btn:hover { background: rgba(255,255,255,0.25); color: white; }
        label { color: #d1d5db; }
    </style>
</head>
<body>
    <!-- Header -->
    <div class="page-header">
        <div class="container d-flex justify-content-between align-items-center">
            <div>
                <h2 class="mb-0 fw-bold">📤 Covert Transmitter</h2>
                <div class="text-light opacity-75" style="font-size:0.85rem;">Blockchain-Verified Network Steganography</div>
            </div>
            <div class="d-flex align-items-center gap-3">
                <div class="stat-card" style="min-width:160px;">
                    <div class="stat-value text-success"><span id="wallet-balance">{{ balance }}</span> <small style="font-size:0.65rem;">ETH</small></div>
                    <div class="stat-label">💰 Wallet Balance</div>
                </div>
                <a href="http://localhost:5000" class="back-btn"><i class="fas fa-arrow-left me-2"></i>Dashboard</a>
            </div>
        </div>
    </div>

    <div class="container pb-5">
        <!-- Wallet Info Strip -->
        <div class="card p-3 mb-4">
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <div class="field-label">Connected Wallet</div>
                    <code style="color:#60a5fa; font-size:0.9rem;">{{ wallet }}</code>
                </div>
                <button class="btn btn-sm btn-outline-secondary" onclick="refreshBalance()"><i class="fas fa-sync-alt me-1"></i>Refresh Balance</button>
            </div>
        </div>

        <!-- Tab Navigation -->
        <ul class="nav nav-pills mb-4" id="senderTabs" role="tablist">
            <li class="nav-item">
                <button class="nav-link active" id="tab-network" data-bs-toggle="pill" data-bs-target="#pane-network">🌐 Network Stego</button>
            </li>
            <li class="nav-item">
                <button class="nav-link" id="tab-blockchain" data-bs-toggle="pill" data-bs-target="#pane-blockchain">⛓️ Blockchain Dead Drop</button>
            </li>
            <li class="nav-item">
                <button class="nav-link" id="tab-p2p" data-bs-toggle="pill" data-bs-target="#pane-p2p">🕸️ P2P Onion Circuit</button>
            </li>
            <li class="nav-item">
                <button class="nav-link" id="tab-security" data-bs-toggle="pill" data-bs-target="#pane-security">🛡️ Security & Access</button>
            </li>
        </ul>

        <div class="tab-content">
            <!-- ===================== Network Steganography ===================== -->
            <div class="tab-pane fade show active" id="pane-network">
                <div class="card p-4">
                    <div class="section-title"><i class="fas fa-satellite-dish text-info"></i> Network Packet Steganography</div>
                    <form id="networkForm">
                        <div class="row g-3 mb-3">
                            <div class="col-md-4">
                                <div class="field-label">Covert Channel</div>
                                <select class="form-select" id="net-method" name="method">
                                    <option value="timing">⏱️ Packet Timing</option>
                                    <option value="size">📦 Packet Size Modulation</option>
                                    <option value="ttl">⏳ TTL Field Encoding</option>
                                    <option value="drift">💨 Infrastructure Silence (Slow-Burn)</option>
                                </select>
                            </div>
                            <div class="col-md-4">
                                <div class="field-label">Target Host IP</div>
                                <input type="text" class="form-control" id="net-host" name="target_host" placeholder="127.0.0.1" required>
                            </div>
                            <div class="col-md-4">
                                <div class="field-label">Options</div>
                                <div class="d-flex gap-3 align-items-center mt-1">
                                    <div class="form-check form-switch">
                                        <input class="form-check-input" type="checkbox" id="net-stealth" name="stealth_mode">
                                        <label class="form-check-label small" for="net-stealth">🤖 Stealth 2.0</label>
                                    </div>
                                    <div class="form-check form-switch">
                                        <input class="form-check-input" type="checkbox" id="net-blockkey" name="block_key">
                                        <label class="form-check-label small" for="net-blockkey">🔑 Block-Hash Key</label>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="mb-3">
                            <div class="field-label">Secret Message</div>
                            <textarea class="form-control" id="net-message" rows="4" placeholder="Enter the hidden message to encode..." required></textarea>
                        </div>
                        <button type="button" class="btn btn-transmit w-100" onclick="sendNetworkStego()">
                            <i class="fas fa-bolt me-2"></i>Transmit via Steganography
                        </button>
                    </form>
                    <div id="net-result" class="result-box"></div>
                </div>
            </div>

            <!-- ===================== Blockchain Dead Drop ===================== -->
            <div class="tab-pane fade" id="pane-blockchain">
                <div class="card p-4">
                    <div class="section-title"><i class="fas fa-link text-warning"></i> Blockchain Dead Drop</div>
                    <div class="mb-4 p-3 rounded" style="background:rgba(245,158,11,0.08); border:1px solid rgba(245,158,11,0.3);">
                        <small class="text-warning"><i class="fas fa-info-circle me-2"></i>Messages are encrypted & stored on Ethereum. The recipient can decrypt offline after the release time.</small>
                    </div>

                    <!-- Compose Drop -->
                    <h6 class="text-muted mb-3">📤 Send Encrypted Drop</h6>
                    <form id="blockchainForm" method="POST" action="http://localhost:5000/dead_drop_send">
                        <div class="row g-3 mb-3">
                            <div class="col-md-6">
                                <div class="field-label">Message</div>
                                <input type="text" class="form-control" id="bc-message" name="message" placeholder="Secret content..." required>
                            </div>
                            <div class="col-md-6">
                                <div class="field-label">Recipient Address</div>
                                <input type="text" class="form-control" id="bc-recipient" name="recipient" placeholder="0x..." required>
                            </div>
                        </div>
                        <div class="row g-3 mb-3">
                            <div class="col-md-6">
                                <div class="field-label">Time-Lock Release (Optional)</div>
                                <input type="datetime-local" class="form-control" id="bc-release" name="release_time">
                                <small class="text-muted">Leave blank for immediate release</small>
                            </div>
                            <div class="col-md-6">
                                <div class="field-label">Encryption Password</div>
                                <input type="password" class="form-control" id="bc-password" name="password" placeholder="Used to encrypt key stored on-chain">
                            </div>
                        </div>
                        <button type="submit" class="btn btn-blockchain w-100">
                            <i class="fas fa-lock me-2"></i>Record to Blockchain
                        </button>
                    </form>

                    <!-- Inbox -->
                    <hr class="border-secondary my-4">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h6 class="text-muted mb-0">📥 Dead Drop Inbox (Your Address)</h6>
                        <button class="btn btn-sm btn-outline-secondary" onclick="loadInbox()"><i class="fas fa-sync-alt me-1"></i>Refresh</button>
                    </div>
                    <div id="bc-inbox" style="max-height:300px; overflow-y:auto;">
                        <div class="text-center text-muted py-3">Click Refresh to load messages</div>
                    </div>
                </div>
            </div>

            <!-- ===================== P2P Onion Routing ===================== -->
            <div class="tab-pane fade" id="pane-p2p">
                <div class="card p-4">
                    <div class="section-title"><i class="fas fa-project-diagram text-info"></i> P2P Onion Circuit Builder</div>
                    <div class="mb-3 p-3 rounded" style="background:rgba(59,130,246,0.08); border:1px solid rgba(59,130,246,0.3);">
                        <small class="text-info"><i class="fas fa-info-circle me-2"></i>Messages are wrapped in multiple encryption layers. Each hop peels a layer, preventing traffic analysis.</small>
                    </div>

                    <div class="row g-3 mb-3">
                        <div class="col-md-4">
                            <div class="field-label">Target Host</div>
                            <input type="text" class="form-control" id="p2p-target" placeholder="127.0.0.1">
                        </div>
                        <div class="col-md-8">
                            <div class="field-label">Secret Message</div>
                            <input type="text" class="form-control" id="p2p-message" placeholder="Hidden content...">
                        </div>
                    </div>

                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h6 class="text-muted mb-0">Relay Hops (Circuit)</h6>
                        <div class="d-flex gap-2">
                            <button class="btn btn-sm btn-outline-info" onclick="discoverNodes()"><i class="fas fa-search me-1"></i>Discover Nodes</button>
                            <button class="btn btn-sm btn-outline-success" onclick="addHop()"><i class="fas fa-plus me-1"></i>Add Hop</button>
                        </div>
                    </div>

                    <div id="nodesFoundBanner" class="d-none mb-3 p-2 rounded" style="background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.3); font-size:0.8rem;">
                        <i class="fas fa-satellite text-success me-2"></i> Found <span id="discovered-count">0</span> verified nodes on chain. Click a node to add as hop.
                        <div id="nodeChips" class="d-flex flex-wrap gap-1 mt-2"></div>
                    </div>

                    <div id="hops-container">
                        <div class="text-center text-muted py-3" id="no-hops-msg"><small>No hops added. Will transmit directly to target.</small></div>
                    </div>

                    <button class="btn btn-transmit w-100 mt-3" onclick="sendP2P()">
                        <i class="fas fa-shield-alt me-2"></i>Send via Onion Circuit
                    </button>
                    <div id="p2p-result" class="result-box"></div>
                </div>
            </div>

            <!-- ===================== Security & Access ===================== -->
            <div class="tab-pane fade" id="pane-security">
                <div class="row g-4">
                    <!-- Whitelist -->
                    <div class="col-md-6">
                        <div class="card p-4 h-100">
                            <div class="section-title"><i class="fas fa-list-check text-success"></i> Sender Whitelist</div>
                            <div class="field-label">Wallet Address to Authorize</div>
                            <div class="input-group mb-2">
                                <input type="text" class="form-control" id="sec-wallet" placeholder="0x...">
                                <button class="btn btn-outline-success" onclick="authorizeWallet()">Authorize</button>
                            </div>
                            <div class="mb-3">
                                <div class="field-label">Duration (seconds, 0 = permanent)</div>
                                <input type="number" class="form-control" id="sec-duration" value="0">
                            </div>
                            <div class="mb-3">
                                <div class="field-label">Reason</div>
                                <input type="text" class="form-control" id="sec-reason" placeholder="e.g., Authorized test user">
                            </div>
                            <div id="sec-result" class="result-box"></div>
                        </div>
                    </div>
                    <!-- Identity Check -->
                    <div class="col-md-6">
                        <div class="card p-4 h-100">
                            <div class="section-title"><i class="fas fa-id-card text-primary"></i> Identity Clearance Check</div>
                            <div class="field-label">Wallet Address</div>
                            <div class="input-group mb-2">
                                <input type="text" class="form-control" id="id-wallet" placeholder="0x...">
                                <button class="btn btn-outline-primary" onclick="checkIdentity()">Verify</button>
                            </div>
                            <div id="id-result" class="result-box mt-2"></div>
                        </div>
                    </div>
                </div>
                <!-- Protocol Switch -->
                <div class="card p-4 mt-4">
                    <div class="section-title"><i class="fas fa-broadcast-tower text-warning"></i> Global Protocol Switch</div>
                    <p class="text-muted small">Changes the active stealth encoding protocol for the entire network via a blockchain transaction.</p>
                    <div class="d-flex gap-3">
                        <button class="btn btn-outline-info flex-grow-1 py-3" onclick="switchProto('timing')"><div class="fs-4">⏱️</div><div class="small fw-bold mt-1">TIMING</div></button>
                        <button class="btn btn-outline-info flex-grow-1 py-3" onclick="switchProto('size')"><div class="fs-4">📦</div><div class="small fw-bold mt-1">SIZE</div></button>
                        <button class="btn btn-outline-info flex-grow-1 py-3" onclick="switchProto('ttl')"><div class="fs-4">⏳</div><div class="small fw-bold mt-1">TTL</div></button>
                        <button class="btn btn-outline-secondary flex-grow-1 py-3" onclick="switchProto('drift')"><div class="fs-4">💨</div><div class="small fw-bold mt-1">DRIFT</div></button>
                    </div>
                    <div id="proto-result" class="result-box mt-3"></div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        let hopCount = 0;

        function showResult(elId, success, message) {
            const el = document.getElementById(elId);
            el.style.display = 'block';
            el.className = 'result-box ' + (success ? 'success' : 'error');
            el.innerHTML = (success ? '✅ ' : '❌ ') + message;
        }

        async function refreshBalance() {
            try {
                const res = await fetch('/balance');
                const data = await res.json();
                document.getElementById('wallet-balance').textContent = parseFloat(data.balance).toFixed(4);
            } catch(e) { console.error(e); }
        }

        async function sendNetworkStego() {
            const method = document.getElementById('net-method').value;
            const host = document.getElementById('net-host').value;
            const message = document.getElementById('net-message').value;
            const stealth = document.getElementById('net-stealth').checked;
            const blockKey = document.getElementById('net-blockkey').checked;
            if (!host || !message) { showResult('net-result', false, 'Please fill in all fields'); return; }

            const form = new FormData();
            form.append('method', method); form.append('target_host', host);
            form.append('secret_data', message);
            if (stealth) form.append('stealth_mode', 'on');
            if (blockKey) form.append('block_key', 'on');

            document.getElementById('net-result').style.display = 'block';
            document.getElementById('net-result').className = 'result-box';
            document.getElementById('net-result').textContent = '⏳ Transmitting...';

            try {
                const res = await fetch('http://localhost:5000/network_hide', { method: 'POST', body: form });
                const text = await res.text();
                if (res.ok) { showResult('net-result', true, 'Transmission sent successfully!'); }
                else { showResult('net-result', false, 'Server error: ' + res.status); }
            } catch(e) { showResult('net-result', false, e.message); }
        }

        async function loadInbox() {
            document.getElementById('bc-inbox').innerHTML = '<div class="text-center text-muted py-3">Loading...</div>';
            try {
                const res = await fetch('http://localhost:5000/dead_drop_check');
                const data = await res.json();
                if (!data.success || !data.messages.length) {
                    document.getElementById('bc-inbox').innerHTML = '<div class="text-center text-muted py-3">No messages found</div>';
                    return;
                }
                document.getElementById('bc-inbox').innerHTML = data.messages.map(m => `
                    <div class="p-3 mb-2 rounded" style="background:#111827; border:1px solid ${m.is_locked ? '#f59e0b' : '#10b981'}33;">
                        <div class="d-flex justify-content-between">
                            <small class="fw-bold text-light">${m.sender.slice(0,10)}...${m.sender.slice(-6)}</small>
                            <span class="badge ${m.is_locked ? 'bg-warning text-dark' : 'bg-success'}">${m.is_locked ? '🔒 LOCKED' : '✅ AVAILABLE'}</span>
                        </div>
                        <div class="small text-muted mt-1">${m.message ? m.message.slice(0,80) + '...' : 'Encrypted'}</div>
                    </div>`).join('');
            } catch(e) { document.getElementById('bc-inbox').innerHTML = '<div class="text-danger small p-2">Error: ' + e.message + '</div>'; }
        }

        async function discoverNodes() {
            try {
                const res = await fetch('http://localhost:5000/api/verified_nodes');
                const data = await res.json();
                const nodes = data.nodes || [];
                document.getElementById('discovered-count').textContent = nodes.length;
                document.getElementById('nodeChips').innerHTML = nodes.map(n =>
                    `<button class="btn btn-sm btn-outline-success" style="font-size:0.7rem;" onclick="addHopFromNode(\'${n.ip}\', \'${n.channels[0] || 'timing'}\')">
                        ${n.ip} (${n.channels[0] || 'timing'})
                    </button>`).join('');
                document.getElementById('nodesFoundBanner').classList.remove('d-none');
            } catch(e) { alert('Error discovering nodes: ' + e.message); }
        }

        function addHopFromNode(ip, channel) { addHop(ip, channel); }

        function addHop(ip='', channel='timing') {
            document.getElementById('no-hops-msg').style.display = 'none';
            const idx = ++hopCount;
            const div = document.createElement('div');
            div.className = 'hop-item'; div.id = 'hop-' + idx;
            div.innerHTML = `<span class="remove-hop" onclick="document.getElementById('hop-${idx}').remove()">✕</span>
                <div class="field-label mb-2">Hop ${idx} Relay</div>
                <div class="row g-2">
                    <div class="col-5"><input type="text" class="form-control form-control-sm" id="hop-ip-${idx}" placeholder="IP Address" value="${ip}"></div>
                    <div class="col-4">
                        <select class="form-select form-select-sm" id="hop-ch-${idx}">
                            <option value="timing" ${channel=='timing'?'selected':''}>⏱️ Timing</option>
                            <option value="size" ${channel=='size'?'selected':''}>📦 Size</option>
                            <option value="ttl" ${channel=='ttl'?'selected':''}>⏳ TTL</option>
                        </select>
                    </div>
                    <div class="col-3"><input type="password" class="form-control form-control-sm" id="hop-sec-${idx}" placeholder="Secret"></div>
                </div>`;
            document.getElementById('hops-container').appendChild(div);
        }

        async function sendP2P() {
            const target = document.getElementById('p2p-target').value;
            const message = document.getElementById('p2p-message').value;
            if (!target || !message) { showResult('p2p-result', false, 'Target and message required'); return; }
            const hops = [];
            document.querySelectorAll('.hop-item').forEach((el, i) => {
                const idx = el.id.replace('hop-', '');
                hops.push({ ip: document.getElementById('hop-ip-'+idx).value, channel: document.getElementById('hop-ch-'+idx).value, secret: document.getElementById('hop-sec-'+idx).value });
            });

            const form = new FormData();
            form.append('method', 'timing'); form.append('target_host', target);
            form.append('secret_data', message);
            if (hops.length) form.append('hops', JSON.stringify(hops));

            showResult('p2p-result', true, 'Sending via P2P circuit...');
            try {
                const res = await fetch('http://localhost:5000/network_hide', { method: 'POST', body: form });
                if (res.ok) { showResult('p2p-result', true, 'Multi-hop transmission complete! Hops: ' + hops.length); }
                else { showResult('p2p-result', false, 'Transmission failed'); }
            } catch(e) { showResult('p2p-result', false, e.message); }
        }

        async function authorizeWallet() {
            const wallet = document.getElementById('sec-wallet').value;
            const duration = document.getElementById('sec-duration').value;
            const reason = document.getElementById('sec-reason').value;
            if (!wallet) { showResult('sec-result', false, 'Wallet address required'); return; }
            try {
                const res = await fetch('http://localhost:5000/api/security/authorize', {
                    method: 'POST', headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ wallet, duration: parseInt(duration), reason })
                });
                const data = await res.json();
                showResult('sec-result', data.success, data.success ? data.message : data.error);
            } catch(e) { showResult('sec-result', false, e.message); }
        }

        async function checkIdentity() {
            const wallet = document.getElementById('id-wallet').value;
            if (!wallet) { showResult('id-result', false, 'Wallet address required'); return; }
            try {
                const res = await fetch('http://localhost:5000/api/registry/status/' + wallet);
                const data = await res.json();
                if (data.success) {
                    showResult('id-result', true, `Org: ${data.organization} | Clearance: ${data.clearance} | Level: ${data.level}`);
                } else { showResult('id-result', false, data.error); }
            } catch(e) { showResult('id-result', false, e.message); }
        }

        async function switchProto(proto) {
            if (!confirm('Switch global network protocol to ' + proto.toUpperCase() + '?')) return;
            try {
                const res = await fetch('http://localhost:5000/api/controller/protocol', {
                    method: 'POST', headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ protocol: proto })
                });
                const data = await res.json();
                showResult('proto-result', data.success, data.success ? 'Protocol switched! TX: ' + data.tx_hash : data.error);
            } catch(e) { showResult('proto-result', false, e.message); }
        }

        refreshBalance();
    </script>
</body>
</html>'''

with open('templates/sender_web.html', 'w', encoding='utf-8') as f:
    f.write(sender_html)

print("✅ Rebuilt sender_web.html with full transmission capabilities")
print("\n📋 Summary of changes:")
print("  1. dashboard.html: Removed 'Covert Transmission Control' block (~235 lines)")
print("  2. dashboard.html: Added live analytics row (balance, protocol, nodes, reputation)")
print("  3. dashboard.html: Added Security Center card + 'Open Sender' CTA")
print("  4. sender_web.html: Full rewrite with 4 tabs:")
print("     - Network Stego (timing/size/ttl/drift)")
print("     - Blockchain Dead Drop (send + inbox)")
print("     - P2P Onion Circuit builder")
print("     - Security & Access (whitelist, identity check, protocol switch)")
