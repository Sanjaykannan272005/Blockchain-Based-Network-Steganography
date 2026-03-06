import time
import json
import os
import hashlib

class InfrastructureDrift:
    """
    Manages the 'Slow-Burn' covert channel by modulating inter-arrival times
    over extremely long durations.
    """
    
    STATE_FILE = "drift_state.json"
    
    def __init__(self, message=None, base_interval=600): # Default 10 mins
        self.message = message
        self.base_interval = base_interval
        self.state = self.load_state()
        
        if message and not self.state:
            self.state = {
                "message": message,
                "binary": self.to_binary(message),
                "current_index": 0,
                "start_time": time.time(),
                "base_interval": base_interval,
                "history": []
            }
            self.save_state()

    def to_binary(self, message):
        return ''.join(format(ord(c), '08b') for c in message)

    def load_state(self):
        if os.path.exists(self.STATE_FILE):
            try:
                with open(self.STATE_FILE, 'r') as f:
                    return json.load(f)
            except:
                return None
        return None

    def save_state(self):
        with open(self.STATE_FILE, 'w') as f:
            json.dump(self.state, f, indent=4)

    def get_next_delay(self):
        """
        Returns the delay for the next packet based on the current bit.
        '0' = -50ms drift
        '1' = +50ms drift
        """
        if not self.state or self.state['current_index'] >= len(self.state['binary']):
            return None
        
        bit = self.state['binary'][self.state['current_index']]
        drift = 0.05 if bit == '1' else -0.05
        
        # Calculate actual interval
        interval = self.state['base_interval'] + drift
        
        # Update state for next bit
        self.state['current_index'] += 1
        self.state['history'].append({
            "bit": bit,
            "drift": drift,
            "timestamp": time.time()
        })
        self.save_state()
        
        return interval

    def get_progress(self):
        if not self.state: return 0
        total = len(self.state['binary'])
        current = self.state['current_index']
        return (current / total) * 100 if total > 0 else 0

if __name__ == "__main__":
    # Example usage for testing
    drift = InfrastructureDrift("SECURE_MSG", base_interval=5) # 5 sec intervals for testing
    print(f"🚀 Initialized Drift Channel: Progress {drift.get_progress()}%")
    
    next_delay = drift.get_next_delay()
    if next_delay:
        print(f"⏱️ Next Packet in: {next_delay}s")
    else:
        print("🏁 Transmission Complete.")
