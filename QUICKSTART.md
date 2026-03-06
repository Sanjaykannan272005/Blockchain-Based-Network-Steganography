# ⚡ Quick Start - Deploy in 10 Minutes

## Step 1: Get API Key (2 min)

1. Go to [infura.io](https://infura.io)
2. Sign up (free)
3. Create new project
4. Copy API key

## Step 2: Setup Environment (1 min)

```bash
copy .env.example .env
notepad .env
```

Fill in:
```env
INFURA_API_KEY=paste_your_key_here
WALLET_ADDRESS=0xYourMetaMaskAddress
PRIVATE_KEY=your_metamask_private_key
```

## Step 3: Install (2 min)

```bash
pip install -r requirements.txt
python load_env.py
```

## Step 4: Deploy Contracts (3 min)

1. Open [remix.ethereum.org](https://remix.ethereum.org)
2. Create file: `DeadDrop.sol`
3. Paste code from `DeadDrop.sol`
4. Compile (Solidity 0.8.0+)
5. Deploy to Sepolia
6. Copy contract address
7. Update `.env`:
   ```env
   DEAD_DROP_CONTRACT=0xYourContractAddress
   ```

## Step 5: Launch (1 min)

```bash
python app.py
```

Open: `http://localhost:5000/dashboard`

## Done! 🎉

**Next Steps:**
- Connect MetaMask
- Send test message
- Explore features

**Need Help?**
- See `DEPLOYMENT_STEPS.md` for detailed guide
- See `CHECKLIST.md` for full deployment checklist
- See `DEPLOY.md` for production deployment

## Common Issues

**"Module not found"**
```bash
pip install -r requirements.txt
```

**"Contract not configured"**
- Deploy contracts first
- Update `.env` with addresses
- Run `python load_env.py`

**"Insufficient funds"**
- Get free Sepolia ETH: [sepoliafaucet.com](https://sepoliafaucet.com)

**"Connection refused"**
- Check Infura API key
- Verify network is Sepolia
