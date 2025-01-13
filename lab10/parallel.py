import time
import math
from multiprocessing import Pool

def is_prime(k, mlp):
    """Check if k is prime using list of small primes"""
    for p in mlp:
        if k % p == 0:
            return False
        if p * p > k:
            return True
    return True

def get_small_primes(r):
    """Generate list of small primes up to sqrt(r)"""
    def is_prime_simple(n):
        if n < 2:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    limit = math.ceil(math.sqrt(r))
    return [i for i in range(2, limit + 1) if is_prime_simple(i)]

def find_twins_in_range(args):
    """Find twin primes in given range"""
    start, end, mlp = args
    twins = []
    for i in range(start, end):
        if is_prime(i, mlp) and is_prime(i + 2, mlp):
            twins.append((i, i + 2))
    return twins

def find_twin_primes_parallel(start, end, num_processes):
    """Main function to find twin primes in parallel"""
    mlp = get_small_primes(end)
    
    chunk_size = (end - start) // num_processes
    ranges = [
        (
            start + i * chunk_size,
            start + (i + 1) * chunk_size if i < num_processes - 1 else end,
            mlp
        )
        for i in range(num_processes)
    ]
    
    with Pool(num_processes) as pool:
        results = pool.map(find_twins_in_range, ranges)
    
    all_twins = []
    for chunk_twins in results:
        all_twins.extend(chunk_twins)
    
    return sorted(all_twins)

if __name__ == '__main__':
    start_range = 1000000
    end_range = 2000000
    num_processes = 8
    
    print(f"Finding twin primes between {start_range} and {end_range}")
    print(f"Using {num_processes} processes")
    
    start_time = time.time()
    twin_primes = find_twin_primes_parallel(start_range, end_range, num_processes)
    end_time = time.time()
    
    print(f"\nFound {len(twin_primes)} twin prime pairs")
    print(f"Time taken: {end_time - start_time:.2f} seconds")
    
    if twin_primes:
        print("\nFirst few twin primes found:")
        for pair in twin_primes[:5]:
            print(pair)