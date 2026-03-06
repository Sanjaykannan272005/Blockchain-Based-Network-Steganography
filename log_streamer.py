import time
import queue
import threading
from datetime import datetime

class LogStreamer:
    """Thread-safe log streamer for SSE"""
    def __init__(self, maxsize=100):
        self.log_queue = queue.Queue(maxsize=maxsize)
        self.clients = []
        self.lock = threading.Lock()

    def emit(self, message, category="INFO"):
        """Add a log message and notify all connected clients"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        formatted_msg = f"[{timestamp}] [{category}] {message}"
        
        # Add to history (internal queue could be used for initial burst)
        # For simplicity, we just push to active client queues
        with self.lock:
            for client_queue in self.clients:
                try:
                    client_queue.put_nowait(formatted_msg)
                except queue.Full:
                    pass # Slow client

    def generate(self):
        """Generator for Flask Response (SSE)"""
        q = queue.Queue(maxsize=50)
        with self.lock:
            self.clients.append(q)
        
        try:
            # Send initial message to confirm connection
            yield f"data: [SYSTEM] Terminal Link Established...\n\n"
            
            while True:
                msg = q.get()
                yield f"data: {msg}\n\n"
        except GeneratorExit:
            with self.lock:
                self.clients.remove(q)
        except Exception as e:
            print(f"Stream Error: {e}")
            with self.lock:
                if q in self.clients:
                    self.clients.remove(q)

# Global instances for each process
streamer = LogStreamer()
