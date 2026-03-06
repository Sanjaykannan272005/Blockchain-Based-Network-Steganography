# 📋 Deployment Checklist

## Pre-Deployment

- [ ] Python 3.8+ installed
- [ ] Git installed
- [ ] MetaMask wallet created
- [ ] Sepolia testnet ETH obtained (from faucet)
- [ ] Infura/Alchemy account created
- [ ] API keys generated

## Configuration

- [ ] Copy `.env.example` to `.env`
- [ ] Fill in `INFURA_API_KEY` in `.env`
- [ ] Fill in `WALLET_ADDRESS` in `.env`
- [ ] Fill in `PRIVATE_KEY` in `.env`
- [ ] Verify `.env` is in `.gitignore`

## Smart Contract Deployment

- [ ] Open Remix IDE (remix.ethereum.org)
- [ ] Deploy `SenderAccessControl.sol`
- [ ] Deploy `DeadDrop.sol`
- [ ] Deploy `StealthRegistry.sol`
- [ ] Copy all contract addresses
- [ ] Update `.env` with contract addresses

## Application Setup

- [ ] Run `pip install -r requirements.txt`
- [ ] Run `python load_env.py` to generate config
- [ ] Test connection: `python test_infura.py`
- [ ] Validate setup: `python validate_system.py`

## Launch

- [ ] Run `python app.py` or `start.bat`
- [ ] Access dashboard at `http://localhost:5000/dashboard`
- [ ] Connect MetaMask wallet
- [ ] Verify blockchain connection (check block number)
- [ ] Test sending a message

## Production (Optional)

- [ ] Set up cloud VM (AWS/GCP/Azure)
- [ ] Configure firewall (allow port 5000 or 443)
- [ ] Install nginx reverse proxy
- [ ] Set up SSL certificate (Let's Encrypt)
- [ ] Use gunicorn: `gunicorn -w 4 app:app`
- [ ] Set up monitoring/logging
- [ ] Configure automatic backups

## Security

- [ ] Never commit `.env` file
- [ ] Never commit `blockchain_config.json`
- [ ] Use separate wallets for test/production
- [ ] Rotate API keys regularly
- [ ] Enable 2FA on all accounts
- [ ] Review smart contract permissions

## Testing

- [ ] Send test message via dashboard
- [ ] Check blockchain explorer for transactions
- [ ] Verify message retrieval
- [ ] Test wallet authentication
- [ ] Test panic button (admin only)
- [ ] Monitor logs for errors

## Troubleshooting

**Can't connect to blockchain:**
- Check RPC URL in `.env`
- Verify API key is valid
- Test with `python test_infura.py`

**Insufficient funds:**
- Get Sepolia ETH from faucet
- Check wallet balance in MetaMask

**Contract not found:**
- Verify contract addresses in `.env`
- Check contracts are deployed on Sepolia

**Port already in use:**
- Change port in `app.py`: `app.run(port=5001)`
- Or kill process using port 5000

## Post-Deployment

- [ ] Document all contract addresses
- [ ] Save deployment transaction hashes
- [ ] Create backup of `.env` (securely)
- [ ] Share dashboard URL with team
- [ ] Set up monitoring alerts
- [ ] Schedule regular security audits

---

**Status**: ⬜ Not Started | 🟡 In Progress | ✅ Complete

**Deployment Date**: _______________
**Deployed By**: _______________
**Environment**: ⬜ Development | ⬜ Staging | ⬜ Production
