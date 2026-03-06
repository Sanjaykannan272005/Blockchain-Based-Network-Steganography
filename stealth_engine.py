import json
import random
import numpy as np
from scipy.stats import norm

class StealthEngine:
    def __init__(self, profile_path='traffic_profile.json'):
        try:
            with open(profile_path, 'r') as f:
                self.profile = json.load(f)
        except:
            # Fallback to defaults if profile missing
            self.profile = {
                "iat_mean": 0.1,
                "iat_std": 0.05,
                "size_mean": 500,
                "size_std": 200,
                "common_sizes": [64, 512, 1024]
            }
            
    def get_stealth_delay(self, bit):
        """
        Generate a delay that mimics normal traffic but encoded with a bit.
        Uses Gaussian distribution shift.
        """
        mean = self.profile['iat_mean']
        std = self.profile['iat_std']
        
        # Shift means slightly (10%) to represent bits
        # Bit 0: Shorter than average
        # Bit 1: Longer than average
        if bit == '0':
            target_mean = mean * 0.8
        else:
            target_mean = mean * 1.2
            
        delay = random.gauss(target_mean, std)
        # Ensure non-negative and within reasonable bounds (3 sigma)
        return max(0.001, min(delay, mean + 3*std))

    def get_stealth_size(self, bit):
        """
        Generate a packet size that mimics normal traffic.
        """
        mean = self.profile['size_mean']
        std = self.profile['size_std']
        
        if bit == '0':
            target_mean = mean * 0.8
        else:
            target_mean = mean * 1.2
            
        size = int(random.gauss(target_mean, std))
        # Clamp to MTU and Ethernet minimum
        return max(64, min(size, 1500))

    def decode_bit(self, observed_value, channel='timing'):
        """
        Use Bayesian inference to guess which bit produced the observed value.
        """
        if channel == 'timing':
            mean = self.profile['iat_mean']
            std = self.profile['iat_std']
        else:
            mean = self.profile['size_mean']
            std = self.profile['size_std']
            
        # Likelyhood of bit 0
        p0 = norm.pdf(observed_value, mean * 0.8, std)
        # Likelyhood of bit 1
        p1 = norm.pdf(observed_value, mean * 1.2, std)
        
        return '0' if p0 > p1 else '1'

if __name__ == "__main__":
    engine = StealthEngine()
    print("Testing Stealth Engine...")
    for bit in ['0', '1']:
        delay = engine.get_stealth_delay(bit)
        decoded = engine.decode_bit(delay, 'timing')
        print(f"Bit {bit} -> Delay {delay:.4f}s -> Decoded {decoded} ({'Correct' if bit==decoded else 'Error'})")
