from scapy.all import sniff, IP
import time
import numpy as np
import json

class TrafficAnalyzer:
    def __init__(self, sample_size=100):
        self.sample_size = sample_size
        self.packet_times = []
        self.packet_sizes = []
        self.last_time = None
        
    def packet_callback(self, pkt):
        if IP in pkt:
            current_time = time.time()
            if self.last_time:
                iat = current_time - self.last_time
                self.packet_times.append(iat)
            
            self.last_time = current_time
            self.packet_sizes.append(len(pkt))
            
            if len(self.packet_sizes) % 10 == 0:
                print(f"Captured {len(self.packet_sizes)}/{self.sample_size} packets...")
                
            if len(self.packet_sizes) >= self.sample_size:
                return True # Stop sniffing
                
    def analyze(self):
        print(f"Starting traffic analysis (Capturing {self.sample_size} IP packets)...")
        # Filters: only IP packets to avoid noise, but general enough to capture "normal" activity
        sniff(prn=self.packet_callback, stop_filter=lambda x: len(self.packet_sizes) >= self.sample_size, timeout=60)
        
        if not self.packet_times:
            return {"error": "No packets captured. Make sure you have network activity."}
            
        stats = {
            "iat_mean": float(np.mean(self.packet_times)),
            "iat_std": float(np.std(self.packet_times)),
            "size_mean": float(np.mean(self.packet_sizes)),
            "size_std": float(np.std(self.packet_sizes)),
            "common_sizes": [int(x) for x in np.unique(self.packet_sizes)[:5]],
            "timestamp": time.time()
        }
        
        with open('traffic_profile.json', 'w') as f:
            json.dump(stats, f, indent=4)
            
        print("\n--- Analysis Complete ---")
        print(json.dumps(stats, indent=4))
        return stats

if __name__ == "__main__":
    analyzer = TrafficAnalyzer(sample_size=100)
    analyzer.analyze()
