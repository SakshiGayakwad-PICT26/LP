from threading import Semaphore, Thread
from time import sleep

# Shared Memory variables
CAPACITY = 10
buffer = [-1 for i in range(CAPACITY)]
in_index = 0
out_index = 0

# Declaring Semaphores
mutex = Semaphore()  # Ensures mutual exclusion for buffer access
empty = Semaphore(CAPACITY)  # Tracks empty slots in the buffer
full = Semaphore(0)  # Tracks full slots in the buffer

class Producer(Thread):
    def run(self):
        global CAPACITY, buffer, in_index, out_index, mutex, empty, full
        items_produced = 0
        counter = 0
        while items_produced < 20:
            empty.acquire()  # Wait for an empty slot
            mutex.acquire()  # Ensure exclusive access to the buffer

            counter += 1
            buffer[in_index] = counter  # Place the item in the buffer
            in_index = (in_index + 1) % CAPACITY  # Update in_index in a circular manner

            print(f"Producer {self.name} produced: {counter}")

            mutex.release()  # Release the mutex after modifying the buffer
            full.release()  # Signal that a new item is available

            sleep(1)  # Simulate time taken to produce an item
            items_produced += 1

class Consumer(Thread):
    def run(self):
        global CAPACITY, buffer, in_index, out_index, mutex, empty, full
        items_consumed = 0
        while items_consumed < 20:
            full.acquire()  # Wait for a full slot
            mutex.acquire()  # Ensure exclusive access to the buffer

            item = buffer[out_index]  # Remove the item from the buffer
            out_index = (out_index + 1) % CAPACITY  # Update out_index in a circular manner

            print(f"Consumer {self.name} consumed item: {item}")

            mutex.release()  # Release the mutex after modifying the buffer
            empty.release()  # Signal that there is an empty slot available

            sleep(2)  # Simulate time taken to consume an item
            items_consumed += 1


# Creating 2 Producer threads
producer1 = Producer()
producer2 = Producer()

# Creating 2 Consumer threads
consumer1 = Consumer()
consumer2 = Consumer()

# Starting the threads
producer1.start()
producer2.start()
consumer1.start()
consumer2.start()

# Waiting for threads to complete
producer1.join()
producer2.join()
consumer1.join()
consumer2.join()
