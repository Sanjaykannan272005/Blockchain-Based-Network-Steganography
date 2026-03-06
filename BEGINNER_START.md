# BEGINNER'S QUICK START GUIDE
# No Blockchain Knowledge Required!

## Step 1: Start the Application

Open terminal in this folder and run:
```
python blockchain_web_app.py
```

Wait for message: "Running on http://127.0.0.1:5000"

## Step 2: Open Your Browser

Visit: http://localhost:5000

You'll see the dashboard with all features.

## Step 3: Send Your First Secret Message (NO SETUP NEEDED!)

1. Click "Messaging" or visit: http://localhost:5000/messaging

2. In the "Send Message" section:
   - Sender Address: Type anything (e.g., "Alice")
   - Message: Type your secret (e.g., "Hello World")
   - Click "Encrypt & Send"

3. Copy the encrypted message that appears

4. In the "Receive Message" section:
   - Paste the encrypted message
   - Click "Decrypt"
   - See your original message!

## That's It! You're Done!

The system uses a built-in simulated blockchain - no external blockchain needed.

---

## What Just Happened?

1. Your message was encrypted with AES-256 (military-grade)
2. A blockchain record was created (simulated locally)
3. The encrypted message can only be decrypted with the right key
4. The blockchain proves when the message was sent

---

## Try the Features

### Feature 1: Control Rules
Visit: http://localhost:5000/feature/1-control
- Set time windows when messages are allowed
- Choose encryption methods

### Feature 2: Trigger Events
Visit: http://localhost:5000/feature/2-triggers
- Create trigger keywords
- Automatically activate features

### Feature 3: Blockchain Keys
Visit: http://localhost:5000/feature/3-keys
- See how keys are derived from blockchain
- Keys change automatically every 15 seconds

### Feature 4: Authentication
Visit: http://localhost:5000/feature/4-auth
- Authenticate users with digital signatures
- Prove who sent a message

---

## Common Questions

**Q: Do I need to install blockchain software?**
A: No! The system has a built-in simulated blockchain.

**Q: Do I need cryptocurrency?**
A: No! This is a simulation for learning.

**Q: Is this secure?**
A: Yes for learning. For production, connect to a real blockchain.

**Q: Can I use this for real secret messages?**
A: This is educational. For real use, deploy to a real blockchain network.

---

## Troubleshooting

**Problem: Port 5000 already in use**
Solution: Edit blockchain_web_app.py, change last line to:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```
Then visit: http://localhost:5001

**Problem: Module not found**
Solution: Run:
```
python -m pip install Flask pycryptodome
```

**Problem: Can't decrypt message**
Solution: Make sure you're using the same system that encrypted it.

---

## Next Steps

1. Try sending multiple messages
2. Explore all 10 features from the dashboard
3. Read BLOCKCHAIN_WEB_README.md for advanced usage
4. Study the code in blockchain_web_app.py

---

## Real-World Use (Advanced)

To connect to a REAL blockchain:

1. Get a free account at Infura.io or Alchemy.com
2. Get your API key
3. Visit: http://localhost:5000/setup
4. Enter your blockchain network details
5. Now your messages are on a real blockchain!

But for learning, the built-in simulation is perfect!

---

Enjoy exploring blockchain steganography! 🚀
