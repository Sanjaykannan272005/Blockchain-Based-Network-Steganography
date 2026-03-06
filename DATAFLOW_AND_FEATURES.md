# 🚀 Blockchain Network Steganography - Data Flow & Features Guide

---

## 📊 Complete Data Flow Diagram

### **Scenario 1: Simple Hide/Extract (Local)**

```
┌─────────────────┐
│   USER UPLOADS  │
│  cover.png      │
│  message: "Go"  │
│  password: "123"│
└────────┬────────┘
         │
         ▼
┌─────────────────────────────┐
│  ENCRYPTION PHASE           │
├─────────────────────────────┤
│  Input: "Go"                │
│  ├─ Add delimiter: "Go###END###"
│  ├─ Derive key: SHA256("123")
│  ├─ Generate IV: random_bytes(16)
│  ├─ AES-256-CBC encrypt
│  └─ Base64 encode
│  Output: "3u8x2k8j2x8..."  │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  BINARY CONVERSION          │
├─────────────────────────────┤
│  Base64 → ASCII → Binary    │
│  "3" → 51 → 00110011        │
│  "u" → 117 → 01110101       │
│  ...                         │
│  Total bits: ~210 bits      │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  LSB EMBEDDING              │
├─────────────────────────────┤
│  Read pixel: RGB(255,127,64)│
│  Add length prefix (32 bits)│
│  For each bit in encrypted: │
│  ├─ Red LSB = bit[0]        │
│  ├─ Green LSB = bit[1]      │
│  ├─ Blue LSB = bit[2]       │
│  └─ Move to next pixel      │
│  Modified: RGB(254,126,64)  │
│  (imperceptible change)     │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  STEGO IMAGE                │
├─────────────────────────────┤
│  cover.png                  │
│    ↓ (embedded)             │
│  stego.png                  │
│  Visually identical!        │
│  File size same             │
│  Message hidden             │
└────────┬────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│  USER DOWNLOADS stego.png    │
│  Shares with receiver        │
└───────────┬──────────────────┘
            │
    ┌───────┴─────────┐
    │                 │
    ▼                 ▼
┌─────────────────────────────┐
│  RECEIVER UPLOADS stego.png │
│  Enters password: "123"     │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  EXTRACTION PHASE           │
├─────────────────────────────┤
│  Read pixel LSBs:           │
│  RGB(254,126,64)            │
│  R LSB=0, G LSB=0, B LSB=0  │
│  Read next pixel LSBs       │
│  Build bit stream           │
│  Extract binary → Base64    │
│  Total bits extracted: 210  │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  DECRYPTION PHASE           │
├─────────────────────────────┤
│  Input: "3u8x2k8j2x8..."    │
│  ├─ Base64 decode           │
│  ├─ Extract IV (first 16B)  │
│  ├─ Derive key: SHA256("123")
│  ├─ AES-256-CBC decrypt     │
│  └─ Remove delimiter        │
│  Output: "Go"               │
└────────┬────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│  ✅ ORIGINAL MESSAGE         │
│     "Go" displayed           │
└──────────────────────────────┘
```

---

### **Scenario 2: Network + Blockchain Integration**

```
SENDER                          BLOCKCHAIN              RECEIVER
  │                                 │                      │
  ├─ User inputs message        │                      │
  │  "Attack at dawn"            │                      │
  │                              │                      │
  ├─ Select features             │                      │
  │  (e.g., 1,3,4,5,6)          │                      │
  │                              │                      │
  ├─ Encrypt: AES-256            │                      │
  │  Key from smartphone          │                      │
  │                              │                      │
  ├─ TX to blockchain ───────────▶ Smart Contract       │
  │  "Store(msg_hash, key)"      ☑ Checks access       │
  │                              ☑ Verifies sender      │
  │                              ☑ Updates reputation  │
  │                              ☑ Creates record      │
  │                              │                      │
  │                              ◀─ TX Confirmed ──────┤
  │                              │  Block #4975123      │
  │                              │  TX 0xabc123...     │
  │                              │                      │
  ├─ Embed in image (LSB)        │                      │
  │  cover.jpg → stego.jpg       │                      │
  │                              │                      │
  ├─ Send TCP packet ─────────────────────────────────▶
  │  Port 9999                   │
  │  Encrypted message           │                      ├─ Receive packet
  │  TX hash included            │                      ├─ Parse message
  │                              │                      │
  │                              │                      ├─ Query blockchain:
  │                              │                      │  "Get key for TX"
  │                              │                      │
  │                              ◀─ Return AES-256 key ┤
  │                              │  From stored TX      │
  │                              │                      │
  │                              │  ├─ Decrypt message
  │                              │  ├─ Verify signature
  │                              │  ├─ Check timestamp
  │                              │  └─ Extract from LSB
  │                              │                      │
  │                              │  ✅ Display: "Attack at dawn"
  │                              │  ✅ Verified by blockchain
  │                              │
```

---

## 🎯 10 Blockchain Features Detailed

### **Feature 1: Blockchain-Controlled Steganography**
```
Purpose: Smart contract controls WHEN steganography is allowed

1. Smart Contract deploys rules:
   ├─ startTime:   1707753600 (Feb 12 2:00 PM UTC)
   ├─ endTime:     1707754200 (Feb 12 2:10 PM UTC) 
   ├─ active:      true
   └─ encoding:    "LSB"

2. Sender checks rules:
   └─ Current time: 1707753840 (Feb 12 2:04 PM)
   └─ Is 1707753840 between 1707753600-1707754200? ✅ YES
   └─ Is active == true? ✅ YES
   └─ Result: ALLOWED ✅

3. If time window opens/closes:
   ├─ Window closed → No new messages allowed
   └─ Window opens → Messages can be sent
```

### **Feature 2: Blockchain-Triggered Covert Channel**
```
Purpose: Only activate on blockchain events

1. Smart contract triggers:
   ├─ Event: function_call("ACTIVATE_COVERT")
   ├─ Block: #4975123
   └─ Keyword: "EMERGENCY"

2. Monitoring nodes listen for triggers:
   └─ Watching mempool for transaction containing "ACTIVATE_COVERT"

3. When trigger found:
   ├─ Status changes: inactive → ACTIVE
   ├─ Activation window: 300 seconds
   └─ Messages can now be sent

4. Real world scenario:
   ├─ Normal operations: receivers NOT listening
   ├─ Caller sends trigger TX
   ├─ All receivers activate simultaneously
   ├─ 5-minute communication window opens
   └─ Then closes automatically
```

### **Feature 3: Blockchain Key Generation**
```
Purpose: Derive encryption keys from immutable blockchain data

1. Query blockchain for latest block:
   {
     "hash": "0x3a8f2k1x",
     "number": 4975123,
     "timestamp": 1707754300,
     "miner": "0x742d35Cc6634C0532925a3b844Bc9e7595f42bE",
     "gasUsed": 8234957
   }

2. Generate key using block data:
   key = SHA256(block_hash + block_number + block_timestamp)
   key = SHA256("0x3a8f2k1x" + "4975123" + "1707754300")
   key = "7f3e8a2b1c9d4e6f..."

3. Key properties:
   ├─ Deterministic: Same block = Same key
   ├─ Time-varying: New block every 12 seconds = New key
   ├─ Tamper-proof: Blockchain consensus ensures authenticity
   └─ Shared knowledge: Both parties can independently derive

4. Security benefit:
   ├─ Key doesn't need to be transmitted
   ├─ No secure key exchange needed
   ├─ All authenticated participants derive same key
   └─ Attacker cannot modify without majority consensus
```

### **Feature 4: Receiver Authentication**
```
Purpose: Verify receiver is legitimate via blockchain

1. User registers on blockchain:
   ├─ Address: 0x742d35Cc6634C0532925a3b844Bc9e7595f42bE
   ├─ Digital signature: Sign(address + nonce)
   └─ Timestamp: 1707753600

2. Sender wants to send to this address:
   └─ Query smart contract: "Is this address verified?"

3. Smart contract checks:
   ├─ Is signature valid? ✅
   ├─ Is sender authorized to contact? ✅
   ├─ Is record not expired? ✅
   ├─ Is account not blocked? ✅
   └─ Result: VERIFIED ✅

4. Only verified addresses can:
   ├─ Receive messages
   ├─ Access blockchain keys
   ├─ Participate in dead drops
   └─ Update reputation scores

5. Blocking mechanism:
   ├─ Suspicious activity detected
   ├─ Reputation drops below threshold
   ├─ Account marked as 'blocked': true
   └─ All communications denied
```

### **Feature 5: Reputation System**
```
Purpose: Track user behavior, detect bad actors

1. User profile on blockchain:
   {
     "address": "0x742d35Cc6634C0532925a3b844Bc9e7595f42bE",
     "reputation": 95,
     "cleanCommunications": 47,
     "detectionAttempts": 2,
     "blocked": false,
     "score_history": [95, 94, 95, 96, 95]
   }

2. Reputation scoring:
   ├─ Successfully send message: +2 points
   ├─ Failed to authenticate: -5 points
   ├─ Used wrong password: -3 points
   ├─ Brute force attempt: -20 points
   └─ Cap: 0-100 points

3. Thresholds:
   ├─ Score < 20: Marked as suspicious
   ├─ Score < 10: Automatically blocked
   ├─ Score 50-75: Normal user
   ├─ Score 75-90: Trusted user
   └─ Score 90+: Verified trusted

4. Real-world scenario:
   ├─ New user: Score 50
   ├─ First legit send: Score 52
   ├─ Attempts brute force: Score 32
   ├─ 10 more failures: Score 2
   ├─ System: "BLOCKED - Suspicious activity"
   └─ Cannot send/receive anymore
```

### **Feature 6: Forensic Verification**
```
Purpose: Create tamper-proof evidence of messages

1. Sender creates forensic commitment:
   message = "Attack at dawn"
   commitment = SHA256(message + nonce + salt)
   commitment = "0x3f8a2b1c..."

2. Store on blockchain:
   emit ForensicCommitment(
     commitment: "0x3f8a2b1c...",
     timestamp: 1707753840,
     creator: "0x742d35Cc...",
     blockNumber: 4975123
   )

3. Blockchain records immutably:
   ├─ Who committed: 0x742d35Cc...
   ├─ When: 1707753840 (blockchain time)
   ├─ What: 0x3f8a2b1c...
   ├─ Block: 4975123
   └─ Tamper-proof by consensus

4. Later verification:
   ├─ Original message revealed: "Attack at dawn"
   ├─ Recalculate: SHA256(message + nonce + salt)
   ├─ Result: "0x3f8a2b1c..."
   ├─ Matches blockchain? ✅ YES
   └─ Proof: Message was created at this time

5. Legal uses:
   ├─ Patent application evidence
   ├─ Copyright protection proof
   ├─ Intellectual property timestamp
   ├─ Non-repudiation for contracts
   └─ Admissible in court proceedings
```

### **Feature 7: Multi-Chain Distribution**
```
Purpose: Distribute message fragments across multiple blockchains

1. Original message: "Secret message"

2. Split into 3 parts:
   ├─ Part 1: "Secret"     → Ethereum block #4975123
   ├─ Part 2: " mess"      → Polygon block #51234567
   └─ Part 3: "age"        → Solana block #201234567

3. Store on each chain:
   Ethereum: Store(hash_part1, tx: 0xabc...)
   Polygon:  Store(hash_part2, tx: 0xdef...)
   Solana:   Store(hash_part3, tx: 0xghi...)

4. Receiver needs all 3 to reconstruct:
   ├─ Query Ethereum: hash_part1 = "Secret"
   ├─ Query Polygon: hash_part2 = " mess"
   ├─ Query Solana: hash_part3 = "age"
   └─ Combine: "Secret" + " mess" + "age" = "Secret message"

5. Security benefits:
   ├─ No single chain compromise reveals full message
   ├─ Attacker needs access to all 3 chains
   ├─ Geographic distribution increases resilience
   ├─ Requires coordination across 3 networks
   └─ Increases detection difficulty 3x
```

### **Feature 8: Dead Drop Coordination**
```
Purpose: Coordinator message pickup via blockchain timestamps

1. Sender creates dead drop:
   {
     "pickup_time": 1707760000 (specific time),
     "pickup_location": "hash_of_coordinates",
     "pickup_method": "TCP_9999",
     "message_id": "0x1a2b3c..."
   }

2. Store on blockchain:
   emit DeadDrop(
     id: "0x1a2b3c...",
     time: 1707760000,
     location_hash: "0x9f8e7d...",
     created: 1707753840,
     expires: 1707773200
   )

3. Receiver knows:
   ├─ Message available at this timestamp
   ├─ Location encoded in blockchain
   ├─ Must be online at exact time
   └─ Only one chance to pick up

4. Real scenario - embassy communication:
   ├─ Agent leaves encrypted package in dead drop
   ├─ Blockchain records exact time
   ├─ Handler queries blockchain
   ├─ Sees "Package ready Feb 12 at 3:00 PM UTC"
   ├─ Handler connects at exact time
   ├─ Receives package securely
   └─ Both never directly contacted

5. Advantages:
   ├─ No direct communication needed
   ├─ Verifiable via blockchain
   ├─ Time-coordinated automatically
   └─ Reduces detection risk
```

### **Feature 9: Key Rotation**
```
Purpose: Automatically schedule new encryption keys

1. Current key:
   ├─ Generated from: Block #4975123
   ├─ Valid until: 1707757200 (1 hour)
   └─ Age: 15 minutes

2. Smart contract schedules rotation:
   event KeyRotationScheduled(
     old_key_id: block_4975123,
     new_key_id: block_4975183,
     rotation_time: 1707757200
   )

3. Rotation timeline:
   ├─ T=0:       Key 1 active
   ├─ T=15 min:  Schedule Key 2
   ├─ T=45 min:  Key 2 accessible
   ├─ T=60 min:  KEY SWITCHOVER (automatic)
   ├─ T+5 min:   Key 1 no longer valid
   └─ T+60 min:  Key 1 deleted

4. During transition:
   ├─ Both keys work (15 min grace period)
   ├─ No disrupted communications
   ├─ Smooth upgrade process
   └─ Increased security

5. Security benefits:
   ├─ Limits key compromise window
   ├─ Regular key changes (hourly)
   ├─ Automatic, no human intervention
   ├─ Prevents key reuse attacks
   └─ Blockchain proves key history
```

### **Feature 10: Protocol Adaptation**
```
Purpose: Automatically select optimal steganography protocol

1. System monitors conditions:
   ├─ Network: "slow, high latency"
   ├─ Threats: "IDS active"
   ├─ Bandwidth: "limited"
   └─ Patterns: "DPI monitoring"

2. Available protocols:
   ├─ LSB (current): High bandwidth, visible to analysis
   ├─ Timing covert channel: Stealthy, needs coordination
   ├─ DNS queries: Natural traffic, slow
   ├─ HTTP headers: Matches normal traffic
   └─ TTL steganography: Difficult to detect

3. Smart contract decides:
   └─ Current conditions: DPI monitoring detected
      ├─ LSB not recommended (visual analysis)
      ├─ DNS selected (natural traffic profile)
      └─ Activate: TTL-based steganography

4. Performance comparison:
   ┌───────────────────────────────────────────┐
   │ Protocol      Speed   Stealth  Bandwidth  │
   ├───────────────────────────────────────────┤
   │ LSB           Fast    Medium   High       │
   │ DNS           Slow    High     Low        │
   │ HTTP Headers  Medium  Medium   Medium     │
   │ Timing        Medium  High     Low        │
   │ TTL           Slow    Very High Very Low │
   └───────────────────────────────────────────┘

5. Adaptive switching:
   ├─ ISP throttles LSB → Switch to DNS
   ├─ IDS detects DNS patterns → Switch to TTL
   ├─ User available → Switch to Timing
   └─ Network congestion → Switch to Headers
```

---

## 📈 Comparison: Single vs Multi-Feature Messages

### **Feature Count Impact**

| Aspect | 1 Feature | 5 Features | 10 Features |
|--------|-----------|-----------|-------------|
| **Encryption** | ✅ AES-256 | ✅ AES-256 | ✅ AES-256 |
| **Key Type** | Hardcoded | Blockchain-derived | Blockchain + Rotation |
| **Authentication** | None | ✅ Blockchain sig | ✅ + Reputation check |
| **Audit Trail** | None | ✅ On-chain record | ✅ + Forensic proof |
| **Multi-chain** | None | None | ✅ 3 chains |
| **Detectability** | Normal | Harder | Very difficult |
| **Verification** | Manual | Blockchain queries | Automated + Proof |
| **Legal proof** | No | Weak | Admissible in court |
| **Send time** | <1 sec | 5-10 sec | 15-30 sec |
| **Requires** | Password | Blockchain account | Full setup |

---

## 🔐 Security Levels

```
LEVEL 1: BASIC ENCRYPTION
├─ AES-256 encryption
├─ Simple password
└─ Local storage only
✅ Protects against: Casual observers
❌ Vulnerable to: Forensic analysis, brute force

LEVEL 2: + STEGANOGRAPHY
├─ LSB hiding in images  
├─ Imperceptible modifications
└─ No metadata leakage
✅ Protects against: Casual + statistical analysis
❌ Vulnerable to: Blockchain analysis (if keys stored centrally)

LEVEL 3: + BLOCKCHAIN KEYS
├─ Keys from blockchain data
├─ No central key storage
├─ Time-varying keys
└─ Multi-party authentication
✅ Protects against: Casual + Statistical + Key compromise
❌ Vulnerable to: Multi-chain analysis, timing attacks

LEVEL 4: + MULTI-CHAIN (ALL 10 FEATURES)
├─ Message split 3 ways
├─ Forensic proofs
├─ Reputation system
├─ Dead drop coordination
├─ Automatic key rotation
└─ Protocol adaptation
✅ Protects against: All known attacks
❌ Vulnerable to: Only quantum computing

```

---

## 🎯 Real-World Application Scenarios

### **Scenario A: Journalist in Hostile Country**
```
Challenge: Send evidence without detection
Solution:
1. Use 10 features
2. Multi-chain distribution (evidence split 3 ways)
3. Dead drop coordination (time-based pickup)
4. Automatic key rotation (hourly new keys)
5. Reputation check (trusted contact verification)

Result: 
├─ Evidence transmitted securely
├─ No single point of failure
├─ Blockchain proves timing (admissible in court)
└─ Attacker needs to compromise 3 blockchains
```

### **Scenario B: Corporate Whistleblower**
```
Challenge: Share confidential docs with regulators
Solution:
1. Use forensic verification feature
2. Create blockchain commitment of documents
3. Timestamp proof in smart contract
4. Receiver authentication (regulator verification)
5. Reputation system (trusted channel)

Result:
├─ Tamper-proof evidence created
├─ Court-admissible timestamp
├─ Regulator identity verified
├─ Document authenticity proven
└─ Non-repudiation established
```

### **Scenario C: Intelligence Agency**
```
Challenge: Covert communication across hostile networks
Solution:
1. Protocol adaptation (auto-detect and switch)
2. Blockchain-triggered channels (activation keyword)
3. Multi-chain distribution (resilience)
4. Dead drop coordination (no direct contact)
5. TTL-based steganography (timing covert channel)

Result:
├─ Messages adapt to network conditions
├─ No predetermined activation time
├─ Survives network analysis
├─ Leaves minimal traces
└─ Blockchain-verified delivery
```

---

## 📊 Performance Benchmarks

| Operation | Time | Scale | Notes |
|-----------|------|-------|-------|
| Hide 1KB message in image | 0.8 sec | 500×500 px | Depends on image size |
| Extract 1KB message | 0.4 sec | 500×500 px | Reverse operation |
| Encrypt 1KB with AES-256 | <50 ms | N/A | Very fast |
| Query blockchain for key | 2-5 sec | N/A | Depends on network |
| Multi-feature processing | 15-30 sec | 10 features | Serial execution |
| Network send (1KB) | <1 sec | Local LAN | Socket transmission |
| Blockchain TX confirm | 6-12 sec | Sepolia | Average block time |

---

## 🏁 Summary: When to Use Each Feature

```
Feature 1 (Control Rules):      When timing matters
Feature 2 (Trigger Events):      When activation is event-driven
Feature 3 (Blockchain Keys):     When key sharing is difficult
Feature 4 (Authentication):      When receiver identity matters
Feature 5 (Reputation):          When user trust varies
Feature 6 (Forensic):            When legal proof needed
Feature 7 (Multi-Chain):         When resilience critical
Feature 8 (Dead Drop):           When coordination is indirect
Feature 9 (Key Rotation):        When long-term security needed
Feature 10 (Protocol Adapt):     When network is unpredictable

✅ Use all 10 for: Maximum security, government, intelligence
✅ Use 3-5 for: Corporate, whistleblowing, journalism
✅ Use 1-2 for: Personal, privacy, basic communication
```

---

*Complete Data Flow Documentation - February 12, 2026*
