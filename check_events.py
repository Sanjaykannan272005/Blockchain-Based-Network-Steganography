import json
from blockchain_integration import BlockchainKeyExchange

with open('blockchain_config.json', 'r') as f:
    config = json.load(f)

b = BlockchainKeyExchange()
b.load_dead_drop_contract(config['dead_drop_contract'])

events = b.get_all_deaddrop_events(limit=5)
print(json.dumps(events, indent=2))
