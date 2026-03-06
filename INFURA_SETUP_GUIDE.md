# 🔑 HOW TO GET INFURA API KEY - STEP BY STEP

## Complete Guide with Screenshots

---

## STEP 1: Visit Infura Website

**Action:** Open your browser and go to:
```
https://infura.io
```

**What you'll see:**
- Infura homepage
- "Get Started for Free" or "Sign Up" button

---

## STEP 2: Sign Up for Free Account

**Action:** Click "Get Started for Free" or "Sign Up"

**You'll see a registration form:**

### Option A: Sign up with Email
1. Enter your email address
2. Create a password
3. Click "Sign Up"

### Option B: Sign up with Google/GitHub
1. Click "Continue with Google" or "Continue with GitHub"
2. Authorize Infura to access your account

**What happens:**
- You'll receive a verification email
- Click the link in the email to verify

---

## STEP 3: Verify Your Email

**Action:** Check your email inbox

**You'll receive:**
- Email from Infura
- Subject: "Verify your email address"
- Click the verification link

**What happens:**
- Browser opens
- "Email verified successfully" message
- Redirected to Infura dashboard

---

## STEP 4: Complete Profile (Optional)

**You may see:**
- "Tell us about yourself" form
- Company name (optional)
- Use case (select "Development" or "Personal Project")

**Action:** Fill in or skip

---

## STEP 5: Create Your First Project

**You'll see the Dashboard:**

**Action:** Click "Create New Project" or "Create New Key"

**Form fields:**
1. **Project Name:** Enter a name (e.g., "Steganography Project")
2. **Network:** Select "Web3 API"
3. Click "Create"

---

## STEP 6: Get Your API Key

**After creating project, you'll see:**

### Project Dashboard showing:

**1. API Keys Section:**
```
API KEY
[Copy icon] 1a2b3c4d5e6f7g8h9i0j...

API KEY SECRET
[Copy icon] a1b2c3d4e5f6g7h8i9j0...
```

**2. Endpoints Section:**
```
HTTPS
https://mainnet.infura.io/v3/YOUR_API_KEY

WebSocket
wss://mainnet.infura.io/ws/v3/YOUR_API_KEY
```

**Action:** Click the copy icon next to "API KEY"

---

## STEP 7: Copy Your API Key

**Your API key looks like:**
```
1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p
```

**It's a 32-character string**

**Action:** 
1. Click copy icon
2. Save it somewhere safe (Notepad, password manager)

---

## STEP 8: Select Network (Important!)

**In your project dashboard:**

**Action:** 
1. Look for "Network Endpoints" dropdown
2. Select **"Sepolia"** (for testing with free ETH)

**Available networks:**
- Mainnet (costs real money)
- **Sepolia** ✅ (FREE - use this!)
- Goerli (being deprecated)
- Polygon
- Arbitrum

**Your Sepolia endpoint:**
```
https://sepolia.infura.io/v3/YOUR_API_KEY
```

---

## STEP 9: Test Your API Key

**Open terminal and test:**

```bash
curl https://sepolia.infura.io/v3/YOUR_API_KEY \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'
```

**Expected response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": "0x123456"
}
```

**If you see this, your API key works!** ✅

---

## STEP 10: Save Your Configuration

**Create file:** `blockchain_config.json`

```json
{
  "infura_api_key": "YOUR_API_KEY_HERE",
  "network": "sepolia",
  "rpc_url": "https://sepolia.infura.io/v3/YOUR_API_KEY_HERE"
}
```

**Replace `YOUR_API_KEY_HERE` with your actual API key!**

---

## 📸 Visual Guide

### What Each Screen Looks Like:

**Screen 1: Homepage**
```
┌─────────────────────────────────────┐
│         INFURA                      │
│                                     │
│  Build on Web3 with confidence      │
│                                     │
│  [Get Started for Free]             │
└─────────────────────────────────────┘
```

**Screen 2: Sign Up**
```
┌─────────────────────────────────────┐
│  Create your account                │
│                                     │
│  Email: [________________]          │
│  Password: [________________]       │
│                                     │
│  [Sign Up]                          │
│                                     │
│  Or continue with:                  │
│  [Google] [GitHub]                  │
└─────────────────────────────────────┘
```

**Screen 3: Dashboard**
```
┌─────────────────────────────────────┐
│  Dashboard                          │
│                                     │
│  My Projects                        │
│  [+ Create New Project]             │
│                                     │
│  No projects yet                    │
└─────────────────────────────────────┘
```

**Screen 4: Create Project**
```
┌─────────────────────────────────────┐
│  Create New Project                 │
│                                     │
│  Name: [Steganography Project]      │
│  Network: [Web3 API ▼]              │
│                                     │
│  [Cancel]  [Create]                 │
└─────────────────────────────────────┘
```

**Screen 5: Project Details (YOUR API KEY HERE!)**
```
┌─────────────────────────────────────┐
│  Steganography Project              │
│                                     │
│  API KEY                            │
│  1a2b3c4d5e6f... [📋 Copy]         │
│                                     │
│  ENDPOINTS                          │
│  Network: [Sepolia ▼]               │
│                                     │
│  HTTPS                              │
│  https://sepolia.infura.io/v3/...   │
│  [📋 Copy]                          │
└─────────────────────────────────────┘
```

---

## ⚠️ IMPORTANT NOTES

### 1. **Keep Your API Key Secret!**
- Don't share it publicly
- Don't commit to GitHub
- Don't post in forums
- Use environment variables

### 2. **Free Tier Limits**
- 100,000 requests per day
- 3 projects
- Enough for development!

### 3. **Network Selection**
- **Sepolia** = FREE test network ✅
- **Mainnet** = Real money ❌
- Always use Sepolia for testing!

---

## 🔧 Troubleshooting

### "Invalid API Key" Error
**Solution:**
- Check you copied the full key
- No extra spaces
- Use the API KEY, not API KEY SECRET

### "Rate Limit Exceeded"
**Solution:**
- Free tier: 100k requests/day
- Wait 24 hours or upgrade

### "Network Not Found"
**Solution:**
- Make sure you selected Sepolia
- Check the endpoint URL is correct

---

## ✅ Quick Checklist

- [ ] Visited https://infura.io
- [ ] Signed up (email or Google/GitHub)
- [ ] Verified email
- [ ] Created new project
- [ ] Named project
- [ ] Selected "Web3 API"
- [ ] Copied API key
- [ ] Selected "Sepolia" network
- [ ] Saved API key securely
- [ ] Tested API key with curl
- [ ] Created blockchain_config.json

---

## 🎯 What You Should Have Now

**1. API Key:**
```
1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p
```

**2. Sepolia Endpoint:**
```
https://sepolia.infura.io/v3/1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p
```

**3. Config File:**
```json
{
  "infura_api_key": "1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p",
  "network": "sepolia",
  "rpc_url": "https://sepolia.infura.io/v3/1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p"
}
```

---

## 🚀 Next Steps

After getting your API key:

1. **Get Test ETH** (next guide)
2. **Deploy Smart Contract**
3. **Update Python code**
4. **Test blockchain integration**

---

## 📞 Need Help?

**Infura Support:**
- Docs: https://docs.infura.io
- Support: https://support.infura.io
- Status: https://status.infura.io

**Common Issues:**
- Email not received? Check spam folder
- Can't create project? Try different browser
- API key not working? Wait 5 minutes after creation

---

**That's it! You now have your Infura API key!** 🎉

**Time needed: 5-10 minutes**
**Cost: FREE** ✅
