class LamportClock:
    def __init__(self, process_id):
        self.clock = 0
        self.process_id = process_id
    
    def local_event(self):
        # Increment clock for a local event
        self.clock += 1
        print(f"Process {self.process_id} - Local event | Clock: {self.clock}")

    def send_event(self):
        # Increment clock for sending a message
        self.clock += 1
        print(f"Process {self.process_id} - Send event | Clock: {self.clock}")
        return self.clock
    
    def receive_event(self, sender_clock):
        # Update clock on receiving a message
        self.clock = max(self.clock, sender_clock) + 1
        print(f"Process {self.process_id} - Receive event | Clock: {self.clock}")

# Example usage
if __name__ == "__main__":
    # Two processes with separate Lamport clocks
    process_A = LamportClock(process_id="A")
    process_B = LamportClock(process_id="B")
    
    # Simulating events in each process
    process_A.local_event()            # Local event in A
    clock_A = process_A.send_event()    # A sends a message
    process_B.receive_event(clock_A)    # B receives the message from A
    
    process_B.local_event()             # Local event in B
    clock_B = process_B.send_event()    # B sends a message
    process_A.receive_event(clock_B)    # A receives the message from B


#NTP
import ntplib
from time import ctime, time

def get_ntp_time(server="pool.ntp.org"):
    try:
        # Get the local system time
        local_time = time()
        print("Local System Time:", ctime(local_time))
        
        # Set up the NTP client and make a request
        client = ntplib.NTPClient()
        response = client.request(server, version=3)
        
        # Get the NTP time and offset
        ntp_time = response.tx_time
        offset = response.offset  # Time difference between local and NTP time
        
        # Print the synchronized NTP time and offset
        print("Synchronized NTP Time:", ctime(ntp_time))
        print("Offset (seconds):", offset)
        
        return ntp_time, offset
    except Exception as e:
        print("Could not synchronize with NTP server:", e)
        return None, None

if __name__ == "__main__":
    get_ntp_time()