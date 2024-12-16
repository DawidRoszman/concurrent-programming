import threading
from typing import List

class PrimesFinder:
    def __init__(self, start: int, end: int, num_threads: int):
        self.start = start
        self.end = end
        self.num_threads = num_threads
        
        self.barrier = threading.Barrier(num_threads + 1)
        
        self.primes: List[int] = []
        
        self.lock = threading.Lock()

    def is_prime(self, k: int) -> bool:
        if k < 2:
            return False
        for i in range(2, int(k**0.5) + 1):
            if k % i == 0:
                return False
        return True

    def find_primes_in_range(self, thread_start: int, thread_end: int):
        local_primes = []
        
        for num in range(thread_start, thread_end + 1):
            if self.is_prime(num):
                local_primes.append(num)
        
        with self.lock:
            self.primes.extend(local_primes)
        
        self.barrier.wait()

    def find_primes(self) -> List[int]:
        thread_range = (self.end - self.start + 1) // self.num_threads
        
        for i in range(self.num_threads):
            thread_start = self.start + i * thread_range
            
            thread_end = (thread_start + thread_range - 1) if i < self.num_threads - 1 else self.end
            
            thread = threading.Thread(
                target=self.find_primes_in_range, 
                args=(thread_start, thread_end)
            )
            thread.start()
        
        self.barrier.wait()
        
        return self.primes

def main():
    start = 2
    end = 100_000_0
    num_threads = 8
    prime_finder = PrimesFinder(start, end, num_threads)
    primes = prime_finder.find_primes()
    
    print(f"Primes in range {start}-{end}:")
    print(primes)
    print(len(primes), "primes found")

if __name__ == "__main__":
    main()
