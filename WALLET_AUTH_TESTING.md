# 🧪 Wallet Authentication Testing Guide

## Overview

This guide walks you through testing all wallet authentication features step-by-step.

---

## Prerequisites

✅ Python 3.8+ installed  
✅ Flask and Web3 installed  
✅ MetaMask browser extension installed  
✅ Sepolia testnet ETH (free from faucet)  
✅ Blockchain RPC URL configured  
✅ Smart contract deployed (SenderAccessControl.sol)  

---

## Part 1: Setup & Startup

### Step 1.1: Install Dependencies
```bash
pip install -r requirements.txt
```

Expected output:
```
Successfully installed web3-6.x.x eth-account-0.x.x flask-2.x.x ...
```

### Step 1.2: Verify Configuration
```bash
python setup_wallet_auth.py
```

Expected output:
```
✅ web3 is installed
✅ eth-account is installed
✅ flask is installed
✅ blockchain_config.json exists
✅ wallet_auth.html template exists
✅ Setup complete! Ready to start wallet authentication.
```

### Step 1.3: Start the Service
```bash
python wallet_auth_app.py
```

Expected output:
```
============================================================
🔐 Wallet Authentication Service
============================================================
📍 Open: http://localhost:5002
🔗 Blockchain: Connected
============================================================
```

### Step 1.4: Access the Web Interface
Open browser and navigate to: `http://localhost:5002`

Expected result:
- Page loads with title "🔐 Wallet Authentication"
- "Connect MetaMask" button is visible
- Wallet status shows: "❌ Wallet Not Connected"

---

## Part 2: Wallet Connection Tests

### Test 2.1: Connect to MetaMask
**Steps:**
1. Click "🪙 Connect MetaMask" button
2. MetaMask popup appears
3. Select account (or click "Next" if only one)
4. Click "Connect" in MetaMask

**Expected Result:**
- MetaMask popup closes
- Page shows: ✅ Wallet Connected
- Your address appears: `0xabc123...6ef789`
- "Disconnect" button becomes enabled
- Console shows: `[WALLET] Connected: 0xabc...`

**Test Passed:** ✅ Wallet connection works

---

### Test 2.2: Verify Connection
**Steps:**
1. Check the wallet status box
2. Copy the address shown

**Expected Result:**
- Address matches your MetaMask account
- Format: `0x` followed by 40 hex characters
- Status is green with checkmark

**Test Passed:** ✅ Correct wallet address displayed

---

## Part 3: Message Signing Tests

### Test 3.1: Sign Default Message
**Steps:**
1. Message field should contain: "Steganography Message Authentication..."
2. Click "✍️ Sign Message"
3. MetaMask popup appears
4. Click "Sign" button

**Expected Result:**
- MetaMask popup shows message to sign
- After signing, popup closes
- Page shows signature in blue box:
  ```
  0x1234567890abcdef1234567890abcdef...
  ```
- Console shows: `[SIGN] ✓ Signature obtained`

**Test Passed:** ✅ Message signing works

---

### Test 3.2: Sign Custom Message
**Steps:**
1. Clear the message field
2. Enter custom message: "Hello, World!"
3. Click "✍️ Sign Message"
4. Approve in MetaMask

**Expected Result:**
- Signature is generated
- Different signature than before (message content matters)
- Format: `0x` followed by hex string
- No errors in console

**Test Passed:** ✅ Custom message signing works

---

### Test 3.3: Cancel Signing
**Steps:**
1. Click "✍️ Sign Message"
2. In MetaMask popup, click "Cancel"

**Expected Result:**
- MetaMask popup closes
- Page doesn't change
- No signature appears
- Console shows: `[ERROR] Signing failed`
- Alert shows: "❌ Message signing cancelled"

**Test Passed:** ✅ Proper error handling

---

## Part 4: Access Control Tests

### Test 4.1: Grant Permanent Access
**Steps:**
1. Scroll to "Access Control Management"
2. Sender Address: Enter a test address (e.g., `0xdef456789...`)
3. Permission Duration: Select "Permanent Access"
4. Reason: Enter "Test sender - QA"
5. Click "✅ Grant Access"

**Expected Result:**
- Alert shows: "✅ Access granted!"
- Message appears in "Active Permissions" list

**Test Passed:** ✅ Permanent access can be granted

---

### Test 4.2: Grant Time-Limited Access
**Steps:**
1. Sender Address: Enter another address
2. Permission Duration: Select "1 Day"
3. Reason: "Temporary access for testing"
4. Click "✅ Grant Access"

**Expected Result:**
- Alert shows: "✅ Access granted!"
- Sender appears in Active Permissions
- Shows time remaining (e.g., "24h remaining")

**Test Passed:** ✅ Time-limited access works

---

### Test 4.3: Check Access Status
**Steps:**
1. Sender Address: Enter address from Test 4.1
2. Click "🔍 Check Access"

**Expected Result:**
- Blue box appears below with result:
  ```
  ✅ Access Allowed
  Address: 0xdef456...
  Granted: [date/time]
  Status: Permanent
  Reason: Test sender - QA
  ```

**Test Passed:** ✅ Access checking works

---

### Test 4.4: Check NonExistent Sender
**Steps:**
1. Sender Address: Enter `0x1111111111111111111111111111111111111111`
2. Click "🔍 Check Access"

**Expected Result:**
- Red box appears:
  ```
  ❌ Access Denied
  Address: 0x111...
  Reason: Sender not in whitelist
  ```

**Test Passed:** ✅ Proper denial for unauthorized senders

---

### Test 4.5: Revoke Access
**Steps:**
1. Sender Address: Enter address from Test 4.1
2. Click "🚫 Revoke Access"

**Expected Result:**
- Alert shows: "✅ Access revoked!"
- Sender disappears from Active Permissions list
- Permission is instantly removed

**Test Passed:** ✅ Access revocation works

---

### Test 4.6: Confirm Revocation
**Steps:**
1. Check access for revoked sender
2. Click "🔍 Check Access"

**Expected Result:**
- Red box appears: "❌ Access Denied"
- Reason: Sender no longer in whitelist

**Test Passed:** ✅ Revocation is persistent

---

## Part 5: Permission Display Tests

### Test 5.1: View Active Permissions
**Steps:**
1. Grant multiple senders access with different durations
2. Scroll to "Active Permissions" section

**Expected Result:**
- All granted senders are listed
- Each shows:
  - Address
  - Reason for access
  - Time remaining (or "Permanent")
  - Date granted
- Permissions are color-coded:
  - 🟦 Blue = Active
  - 🟨 Yellow = Expires soon (<1 day)
  - 🟥 Red = Expired

**Test Passed:** ✅ Permission list displays correctly

---

### Test 5.2: Permission Countdown
**Steps:**
1. Grant access for "1 Day"
2. Watch the "Active Permissions" section for several seconds

**Expected Result:**
- Time badge updates every second
- Format changes from "1d" → "23h 59m" → "23h 58m" etc.
- Countdown is accurate

**Test Passed:** ✅ Countdown timer works

---

## Part 6: Authentication Flow Tests

### Test 6.1: Full Authentication (Success)
**Steps:**
1. Grant access to sender: `0xaabbccddeeff...` with 1-day duration
2. Sign a message
3. Observe authentication result

**Expected Result:**
- Green box shows: "✅ Authentication Successful!"
- Details show:
  ```
  Sender: 0xaabbcc...
  Status: Temporary
  Expires: [date/time]
  Time Remaining: 23 hours 45 minutes
  ```

**Test Passed:** ✅ Full auth flow works

---

### Test 6.2: Authentication (No Access)
**Steps:**
1. Your connected wallet is NOT in whitelist
2. Try to sign message with another sender's address
3. Observe result

**Expected Result:**
- Red box shows: "❌ Authentication Failed"
- Reason: "Sender not in whitelist"

**Test Passed:** ✅ Prevents unauthorized senders

---

### Test 6.3: Authentication (Permission Expired)
**Steps:**
1. Grant access for "1 Day"
2. In browser console, set current time 25 hours in future
   ```javascript
   // Modify the check in backend or manually expire
   ```
3. Check access status

**Expected Result:**
- Red box shows: "❌ Access Denied"
- Reason: "Access expired"

**Test Passed:** ✅ Expiration is enforced

---

## Part 7: Error Handling Tests

### Test 7.1: Invalid Wallet Address
**Steps:**
1. Sender Address: Enter `12345` (invalid)
2. Click "🔍 Check Access"

**Expected Result:**
- Error handling occurs
- Web page remains stable
- No crash or frozen UI

**Test Passed:** ✅ Input validation works

---

### Test 7.2: Missing Fields
**Steps:**
1. Leave Sender Address empty
2. Click "✅ Grant Access"

**Expected Result:**
- Alert shows: "❌ Please enter sender address"
- Nothing is granted

**Test Passed:** ✅ Form validation works

---

### Test 7.3: Network Disconnection
**Steps:**
1. Turn off internet connection (or unplug network)
2. Try to check access
3. Turn internet back on

**Expected Result:**
- Error shown in blue box
- Network recovers gracefully
- Can retry after reconnection

**Test Passed:** ✅ Network resilience

---

## Part 8: Integration Tests

### Test 8.1: Multiple Wallets
**Steps:**
1. Open MetaMask settings
2. Switch to different account
3. Click "Disconnect"
4. Reconnect to new account

**Expected Result:**
- New address is shown
- Previous permissions still exist in system
- Can grant/revoke for different account

**Test Passed:** ✅ Multi-wallet support works

---

### Test 8.2: Persistent State
**Steps:**
1. Grant access to multiple senders
2. Open browser DevTools
3. Refresh the page (Ctrl+R)

**Expected Result:**
- All permissions are still there
- List is populated on page load
- No data loss

**Test Passed:** ✅ Data persistence works

---

## Part 9: Performance Tests

### Test 9.1: Response Time
**Steps:**
1. Open browser DevTools (F12)
2. Go to "Network" tab
3. Click "✅ Grant Access"
4. Observe request time

**Expected Result:**
- Request completes in <1 second
- No timeouts
- Response is immediate

**Test Passed:** ✅ Good performance

---

### Test 9.2: Large Permission List
**Steps:**
1. Grant access to 50+ different addresses
2. Scroll through Active Permissions list
3. Try to grant/revoke more access

**Expected Result:**
- Page remains responsive
- List renders smoothly
- No freezing or lag
- All operations complete quickly

**Test Passed:** ✅ Scales well

---

## Part 10: Security Tests

### Test 10.1: Signature Verification
**Steps:**
1. Sign a message
2. Manually alter the signature in the console
   ```javascript
   document.getElementById('signatureText').innerText = '0x1234...';
   ```
3. Try to authenticate with altered signature

**Expected Result:**
- Backend rejects invalid signature
- Error: "Signature verification failed"
- No access is granted

**Test Passed:** ✅ Signature tampering detected

---

### Test 10.2: Address Spoofing
**Steps:**
1. Sign message with account A
2. Manually change signer address to account B
3. Submit to /verify_signature

**Expected Result:**
- Backend detects mismatch
- Error: "Signature does not match signer"
- No access granted

**Test Passed:** ✅ Spoofing prevention works

---

### Test 10.3: Replay Attack Prevention
**Steps:**
1. Get valid signature for message
2. Try to use same signature again
3. Try different sender address with old signature

**Expected Result:**
- Signature is valid only for original signer
- Cannot replay with different address
- System is secure against replay

**Test Passed:** ✅ Replay attacks prevented

---

## Test Summary

### All Tests Passed Checklist

```
Part 1: Setup & Startup
  ☐ Dependencies installed
  ☐ Configuration verified
  ☐ Service started
  ☐ Web interface loaded

Part 2: Wallet Connection
  ☐ Connect to MetaMask
  ☐ Verify correct address
  
Part 3: Message Signing
  ☐ Sign default message
  ☐ Sign custom message
  ☐ Cancel signing

Part 4: Access Control
  ☐ Grant permanent access
  ☐ Grant time-limited access
  ☐ Check access status
  ☐ Check nonexistent sender
  ☐ Revoke access
  ☐ Confirm revocation

Part 5: Permission Display
  ☐ View active permissions
  ☐ Permission countdown

Part 6: Authentication Flow
  ☐ Full auth (success)
  ☐ Auth (no access)
  ☐ Auth (expired)

Part 7: Error Handling
  ☐ Invalid address
  ☐ Missing fields
  ☐ Network disconnection

Part 8: Integration
  ☐ Multiple wallets
  ☐ Persistent state

Part 9: Performance
  ☐ Response time
  ☐ Large permission list

Part 10: Security
  ☐ Signature verification
  ☐ Address spoofing
  ☐ Replay attack prevention
```

---

## Troubleshooting

### Issue: "MetaMask not installed"
**Solution:**
1. Install MetaMask browser extension
2. Refresh the page
3. Click "Connect MetaMask" again

### Issue: "Signature verification failed"
**Solution:**
1. Make sure you're signing with the connected wallet
2. Don't modify the message after signing
3. Check that signature string is complete (not truncated)

### Issue: "Access Denied" when checking access
**Solution:**
1. Owner must have granted your address access
2. Check that access hasn't expired
3. Verify you're checking the correct address

### Issue: "Cannot connect to blockchain"
**Solution:**
1. Check RPC URL in blockchain_config.json
2. Verify internet connection
3. Check RPC endpoint status
4. Try different RPC provider (Alchemy, QuickNode, etc.)

---

## Success Criteria

✅ All 50+ test cases pass  
✅ No console errors (F12 → Console)  
✅ No network errors (F12 → Network)  
✅ UI remains responsive throughout  
✅ All features work as designed  
✅ Security tests prevent abuse  
✅ Data persists across sessions  

---

## Next Steps After Testing

1. ✅ Fix any failed tests
2. ✅ Test integration with sender/receiver apps
3. ✅ Deploy smart contract to production
4. ✅ Update blockchain_config.json with mainnet contract
5. ✅ Run end-to-end testing with real users
6. ✅ Monitor for any production issues

---

**Test Suite Version**: 1.0  
**Last Updated**: February 14, 2026  
**Status**: Ready for Testing ✅
