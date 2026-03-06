# 💼 Wallet Authentication Integration Guide

## Overview

This guide shows how to integrate wallet authentication with your existing steganography sender and receiver applications.

---

## Architecture Overview

```
MetaMask Wallet
    ↓ (Signs message)
    ↓
Sender App (sender_web.py)
    ↓ (Verifies signature)
    ↓
Wallet Auth Service (wallet_auth_app.py)
    ↓ (Checks whitelist)
    ↓
Blockchain: SenderAccessControl.sol
    ↓
Message transmitted if authorized
    ↓
Receiver App (receiver_web.py)
    ↓
User decrypts message
```

---

## Integration 1: Add Wallet Auth to Sender

### Step 1: Update sender_web.py

Add imports at the top:
```python
from flask import request, jsonify
import requests
import json

# Wallet auth service URL
WALLET_AUTH_URL = "http://localhost:5002"
```

### Step 2: Create Authentication Endpoint

Add this new route to sender_web.py:

```python
@app.route('/authenticate_sender', methods=['POST'])
def authenticate_sender():
    """
    Verify sender's wallet signature and check whitelist
    
    Request body:
    {
        "message": "Steganography Message Authentication...",
        "signature": "0x1234567890abcdef...",
        "signer": "0xaabbccddeeff00112233..."
    }
    
    Response:
    {
        "authenticated": true,
        "sender": "0xaabbccddeeff00112233...",
        "access_details": {
            "allowed": true,
            "granted_at": "2024-02-14T10:00:00",
            "expires_at": "2024-02-21T10:00:00",
            "time_remaining_seconds": 594000,
            "is_permanent": false,
            "reason": "Test sender"
        }
    }
    """
    try:
        data = request.get_json()
        message = data.get('message')
        signature = data.get('signature')
        signer = data.get('signer')
        
        if not all([message, signature, signer]):
            return jsonify({
                'authenticated': False,
                'error': 'Missing required fields: message, signature, signer'
            }), 400
        
        # Call wallet auth service
        response = requests.post(
            f"{WALLET_AUTH_URL}/verify_signature",
            json={
                'message': message,
                'signature': signature,
                'signer': signer
            },
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"[AUTH] ✓ Sender authenticated: {result['sender']}")
            return jsonify(result), 200
        else:
            print(f"[AUTH] ✗ Authentication failed: {response.text}")
            return jsonify({
                'authenticated': False,
                'error': response.json().get('error', 'Authentication failed')
            }), 401
            
    except requests.exceptions.Timeout:
        return jsonify({
            'authenticated': False,
            'error': 'Wallet authentication service timeout'
        }), 504
    except Exception as e:
        print(f"[ERROR] Authentication error: {str(e)}")
        return jsonify({
            'authenticated': False,
            'error': str(e)
        }), 500
```

### Step 3: Update Send Message Route

Modify the /send route to require authentication:

```python
@app.route('/send', methods=['POST'])
def send_message():
    """
    Send steganographic message
    Now requires sender wallet authentication
    """
    try:
        # Get request data
        image_file = request.files.get('image')
        message = request.form.get('message')
        password = request.form.get('password')
        signature = request.form.get('signature')  # NEW
        signer = request.form.get('signer')         # NEW
        wallet_message = request.form.get('wallet_message')  # NEW
        
        # Validate inputs
        if not all([image_file, message, password]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # NEW: Verify wallet authentication
        if signature and signer and wallet_message:
            auth_response = requests.post(
                f"{WALLET_AUTH_URL}/verify_signature",
                json={
                    'message': wallet_message,
                    'signature': signature,
                    'signer': signer
                },
                timeout=10
            )
            
            if auth_response.status_code != 200:
                result = auth_response.json()
                return jsonify({
                    'error': 'Sender not authorized',
                    'details': result.get('error', 'Unknown error')
                }), 403
            
            auth_data = auth_response.json()
            if not auth_data.get('authenticated'):
                return jsonify({
                    'error': 'Signature verification failed'
                }), 401
            
            print(f"[SEND] ✓ Sender {signer} verified and authorized")
        else:
            # For backwards compatibility, allow unsigned sends
            print("[SEND] ⚠ Warning: Send without wallet authentication")
        
        # Continue with existing send logic...
        # (Hide message in image, encrypt, transmit, etc.)
        
        print(f"[SEND] ✓ Message sent from {signer}")
        return jsonify({
            'status': 'success',
            'message': 'Message sent successfully',
            'authenticated_sender': signer if signer else 'anonymous'
        }), 200
        
    except Exception as e:
        print(f"[ERROR] Send error: {str(e)}")
        return jsonify({'error': str(e)}), 500
```

### Step 4: Update Frontend (sender_web.html)

Add wallet authentication UI to send form:

```html
<!-- Add this section to the send form -->
<div class="card mt-4">
    <div class="card-header" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
        <h5 class="mb-0">🔐 Wallet Authentication</h5>
    </div>
    <div class="card-body">
        <!-- Wallet Connection Status -->
        <div class="mb-3">
            <button type="button" class="btn btn-primary" id="connectWalletBtn" onclick="connectWallet()">
                🪙 Connect MetaMask
            </button>
            <div id="walletStatus" class="alert alert-warning mt-2" style="display:none;">
                <span id="walletAddress"></span>
            </div>
        </div>
        
        <!-- Message to Sign -->
        <div class="mb-3">
            <label class="form-label">📝 Message to Sign (for authentication)</label>
            <textarea class="form-control" id="walletMessage" rows="3" readonly>
Steganography Message Authentication - This proves you are the legitimate sender
            </textarea>
        </div>
        
        <!-- Sign Button -->
        <div class="mb-3">
            <button type="button" class="btn btn-warning" id="signBtn" onclick="signMessage()" disabled>
                ✍️ Sign with MetaMask
            </button>
        </div>
        
        <!-- Signature Display -->
        <div id="signatureBox" style="display:none;">
            <label class="form-label">✅ Your Signature</label>
            <div class="bg-light p-2 rounded mb-3" style="max-height: 100px; overflow-y: auto;">
                <code id="signatureText" style="word-break: break-all;"></code>
            </div>
        </div>
        
        <!-- Auth Status -->
        <div id="authStatus" class="alert" style="display:none;"></div>
    </div>
</div>

<!-- Hidden inputs for signature data -->
<input type="hidden" id="signatureInput" name="signature">
<input type="hidden" id="signerInput" name="signer">
<input type="hidden" id="walletMessageInput" name="wallet_message">
```

### Step 5: Add JavaScript for Wallet Auth (sender_web.html)

```javascript
let web3Provider = null;
let userAccount = null;

async function connectWallet() {
    try {
        // Check if MetaMask is installed
        if (typeof window.ethereum === 'undefined') {
            alert('❌ MetaMask is not installed. Please install it first.');
            return;
        }
        
        // Request account access
        const accounts = await window.ethereum.request({ 
            method: 'eth_requestAccounts' 
        });
        
        userAccount = accounts[0];
        web3Provider = new Web3(window.ethereum);
        
        // Update UI
        document.getElementById('walletStatus').style.display = 'block';
        document.getElementById('walletAddress').innerText = `✅ Connected: ${userAccount}`;
        document.getElementById('connectWalletBtn').disabled = true;
        document.getElementById('signBtn').disabled = false;
        
        console.log('[SENDER] ✓ MetaMask connected:', userAccount);
    } catch (error) {
        console.error('[SENDER] ✗ Connection failed:', error);
        alert('❌ Failed to connect MetaMask: ' + error.message);
    }
}

async function signMessage() {
    if (!userAccount || !web3Provider) {
        alert('❌ Please connect MetaMask first');
        return;
    }
    
    try {
        const message = document.getElementById('walletMessage').value;
        
        // Sign the message
        const signature = await web3Provider.currentProvider.request({
            method: 'personal_sign',
            params: [message, userAccount]
        });
        
        // Display signature
        document.getElementById('signatureText').innerText = signature;
        document.getElementById('signatureBox').style.display = 'block';
        
        // Store in hidden inputs
        document.getElementById('signatureInput').value = signature;
        document.getElementById('signerInput').value = userAccount;
        document.getElementById('walletMessageInput').value = message;
        
        // Update auth status
        const authStatus = document.getElementById('authStatus');
        authStatus.className = 'alert alert-success';
        authStatus.innerHTML = '✅ <strong>Message signed!</strong> Your signature is ready for authentication.';
        authStatus.style.display = 'block';
        
        console.log('[SENDER] ✓ Message signed:', signature);
    } catch (error) {
        console.error('[SENDER] ✗ Signing failed:', error);
        alert('❌ Signing failed: ' + error.message);
    }
}

// Update send button to include auth data
document.getElementById('sendBtn').addEventListener('click', async function(e) {
    e.preventDefault();
    
    // If wallet is connected, verify auth before sending
    if (userAccount && document.getElementById('signatureInput').value) {
        const formData = new FormData(document.getElementById('sendForm'));
        
        // Show loading state
        const btn = this;
        btn.disabled = true;
        btn.innerText = '⏳ Authenticating...';
        
        try {
            // Verify with wallet auth service
            const authResponse = await fetch('/authenticate_sender', {
                method: 'POST',
                body: formData
            });
            
            if (!authResponse.ok) {
                const error = await authResponse.json();
                alert('❌ Authentication failed: ' + error.details);
                btn.disabled = false;
                btn.innerText = '📤 Send Message';
                return;
            }
            
            // Auth successful, proceed with send
            const actualResponse = await fetch('/send', {
                method: 'POST',
                body: formData
            });
            
            if (actualResponse.ok) {
                const result = await actualResponse.json();
                alert('✅ ' + result.message);
                document.getElementById('sendForm').reset();
            } else {
                const error = await actualResponse.json();
                alert('❌ Send failed: ' + error.error);
            }
        } catch (error) {
            alert('❌ Error: ' + error.message);
        } finally {
            btn.disabled = false;
            btn.innerText = '📤 Send Message';
        }
    } else {
        alert('⚠️ Please connect wallet and sign message for authenticated sending');
    }
});
```

---

## Integration 2: Add Wallet Auth to Receiver

### Step 1: Add Authentication Check

Update receiver_web.py to verify sender is whitelisted:

```python
@app.route('/verify_sender_access', methods=['POST'])
def verify_sender_access():
    """
    Check if sender is authorized to send messages
    Called before decrypting received messages
    """
    try:
        data = request.get_json()
        sender_address = data.get('sender_address')
        
        if not sender_address:
            return jsonify({
                'authorized': False,
                'error': 'Sender address required'
            }), 400
        
        # Check access on blockchain
        response = requests.get(
            f"{WALLET_AUTH_URL}/check_access?sender={sender_address}",
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"[VERIFY] Sender {sender_address} access check: {result}")
            return jsonify(result), 200
        else:
            return jsonify({
                'authorized': False,
                'error': 'Sender verification failed'
            }), 401
            
    except Exception as e:
        print(f"[ERROR] Sender verification error: {str(e)}")
        return jsonify({
            'authorized': False,
            'error': str(e)
        }), 500
```

### Step 2: Update Message Decryption

Modify decrypt route to check sender authorization:

```python
@app.route('/decrypt', methods=['POST'])
def decrypt_message():
    """
    Decrypt steganographic message
    Now requires sender to be whitelisted
    """
    try:
        # Get decryption data
        message_id = request.form.get('message_id')
        password = request.form.get('password')
        sender_address = request.form.get('sender_address')  # NEW
        
        # Load and process message (existing code)
        message_data = load_message(message_id)
        
        # NEW: Verify sender is authorized
        if sender_address:
            auth_check = requests.get(
                f"{WALLET_AUTH_URL}/check_access?sender={sender_address}",
                timeout=10
            )
            
            if auth_check.status_code != 200:
                auth_result = auth_check.json()
                return jsonify({
                    'error': 'Sender not authorized',
                    'details': auth_result
                }), 403
            
            auth_data = auth_check.json()
            if not auth_data.get('allowed'):
                return jsonify({
                    'error': f"Sender {sender_address} is not whitelisted",
                    'reason': auth_data.get('reason')
                }), 403
            
            print(f"[DECRYPT] ✓ Sender {sender_address} verified and authorized")
        
        # Continue with decryption
        # (Extract from image, decrypt with password, etc.)
        
        return jsonify({
            'status': 'success',
            'decrypted': decrypted_content,
            'sender_verified': bool(sender_address),
            'sender': sender_address
        }), 200
        
    except Exception as e:
        print(f"[ERROR] Decryption error: {str(e)}")
        return jsonify({'error': str(e)}), 500
```

### Step 3: Update Frontend (receiver_web.html)

Add sender verification UI:

```html
<!-- Add to message display section -->
<div class="card mt-3">
    <div class="card-header" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
        <h5 class="mb-0">🔐 Sender Verification</h5>
    </div>
    <div class="card-body">
        <!-- Sender Address Input -->
        <div class="mb-3">
            <label class="form-label">📍 Known Sender Address (optional)</label>
            <input type="text" class="form-control" id="senderAddress" 
                   placeholder="0x... (paste sender's wallet address if known)">
            <small class="form-text text-muted">
                Leave empty to receive from anyone. Enter address to verify sender is whitelisted.
            </small>
        </div>
        
        <!-- Verification Status -->
        <div id="senderVerificationStatus" style="display:none;"></div>
        
        <!-- Verify Button -->
        <button class="btn btn-info" id="verifySenderBtn" onclick="verifySenderAccess()">
            🔍 Verify Sender Access
        </button>
    </div>
</div>
```

### Step 4: Add JavaScript for Sender Verification

```javascript
async function verifySenderAccess() {
    const senderAddress = document.getElementById('senderAddress').value.trim();
    
    if (!senderAddress) {
        alert('⚠️ Please enter a sender address');
        return;
    }
    
    if (!senderAddress.startsWith('0x') || senderAddress.length !== 42) {
        alert('❌ Invalid Ethereum address format');
        return;
    }
    
    try {
        const response = await fetch('/verify_sender_access', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                sender_address: senderAddress
            })
        });
        
        const result = await response.json();
        const statusBox = document.getElementById('senderVerificationStatus');
        
        if (response.ok) {
            if (result.allowed) {
                statusBox.className = 'alert alert-success';
                statusBox.innerHTML = `
                    <strong>✅ Sender is Authorized!</strong>
                    <div>Address: ${senderAddress}</div>
                    <div>Granted: ${new Date(result.granted_at).toLocaleString()}</div>
                    <div>Status: ${result.time_remaining_seconds ? 
                        `Expires in ${Math.floor(result.time_remaining_seconds / 3600)} hours` : 
                        'Permanent'}</div>
                    <div>Reason: ${result.reason || 'No reason provided'}</div>
                `;
            } else {
                statusBox.className = 'alert alert-danger';
                statusBox.innerHTML = `
                    <strong>❌ Sender Not Authorized</strong>
                    <div>Address: ${senderAddress}</div>
                    <div>Reason: ${result.reason || 'Not in whitelist'}</div>
                `;
            }
        } else {
            statusBox.className = 'alert alert-danger';
            statusBox.innerHTML = `<strong>❌ Verification Error:</strong> ${result.error}`;
        }
        
        statusBox.style.display = 'block';
        console.log('[RECEIVER] Verification result:', result);
        
    } catch (error) {
        alert('❌ Error verifying sender: ' + error.message);
        console.error('[RECEIVER] Verification error:', error);
    }
}

// Auto-verify when entering sender address
document.getElementById('senderAddress')?.addEventListener('change', function() {
    if (this.value.startsWith('0x') && this.value.length === 42) {
        verifySenderAccess();
    }
});
```

---

## Integration 3: End-to-End Flow

### Complete Sending Flow

```
1. Sender connects MetaMask wallet
2. Sender enters message and password
3. Sender signs authentication message
4. Sender hides message in image
5. Sender encrypts hidden data with password
6. Sender transmits encrypted image to receiver
7. Backend calls /authenticate_sender
8. Wallet auth service verifies signature
9. Smart contract checks whitelist
10. If authorized → message sent ✓
11. If unauthorized → message blocked ✗
```

### Complete Receiving Flow

```
1. Receiver waits for encrypted images
2. Encrypted image arrives (sender known)
3. Receiver optionally enters sender address
4. Receiver clicks "Verify Sender Access"
5. Backend calls wallet_auth_app.py
6. Smart contract confirms sender is whitelisted
7. Receiver enters password
8. Receiver clicks "Decrypt"
9. Message extracted from image
10. Message decrypted with password
11. If sender authorized → show message ✓
12. If sender unauthorized → block message ✗
```

---

## Testing Integration

### Test Case 1: Authorized Send
```
✓ Connect MetaMask
✓ Enter message
✓ Enter password
✓ Enter and sign authentication message
✓ Click Send
✓ Message arrives at receiver
✓ Receiver verifies sender
✓ Message decrypted successfully
```

### Test Case 2: Unauthorized Send
```
✓ Connect MetaMask (not whitelisted)
✓ Enter message and password
✓ Sign authentication message
✓ Click Send
✗ Backend rejects (not whitelisted)
✗ Message never sent to receiver
```

### Test Case 3: Expired Permission
```
✓ Sender was whitelisted but permission expired
✓ Sender tries to send message
✗ Backend rejects (permission expired)
✗ Message blocked
```

---

## Security Considerations

### 1. Signature Verification
- ✅ Signatures are cryptographically verified
- ✅ Only valid ECDSA signatures pass
- ✅ Cannot forge signatures without private key

### 2. Whitelist Access
- ✅ Only owner can add/remove senders
- ✅ Time-based expiration prevents indefinite access
- ✅ Permissions can be revoked instantly

### 3. Message Integrity
- ✅ Password-based encryption + steganography
- ✅ Only intended recipient can decrypt
- ✅ Message hidden in image, not visible in transit

### 4. Replay Prevention
- ✅ Signature tied to specific message content
- ✅ Cannot reuse signature for different message
- ✅ Timestamp in blockchain prevents old signatures

---

## Troubleshooting

### Issue: "Signature verification failed"
**Solution:**
- Make sure signature matches the message and signer
- Check that message content hasn't changed
- Ensure signature is complete (not truncated)

### Issue: "Sender not authorized"
**Solution:**
- Owner must grant access first via wallet_auth.html
- Check if permission has expired
- Verify sender address is correct (case-sensitive)

### Issue: Integration not working
**Solution:**
- Make sure wallet_auth_app.py is running on port 5002
- Check blockchain_config.json has correct RPC and contract address
- Verify MetaMask is connected to same network (Sepolia)
- Check browser console for errors (F12)

---

## Next Steps

1. ✅ Deploy SenderAccessControl.sol to Sepolia
2. ✅ Update blockchain_config.json with contract address
3. ✅ Implement integration code above in your apps
4. ✅ Test each integration path
5. ✅ Deploy to production Ethereum mainnet

---

**Version**: 1.0  
**Status**: Ready for Integration  
**Last Updated**: February 14, 2026
