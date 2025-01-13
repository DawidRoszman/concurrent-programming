import time
import math

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

def find_twin_primes_sequential(start, end):
    """Find twin primes in given range using sequential approach"""
    # Get small primes first
    mlp = get_small_primes(end)
    
    # Find twin primes
    twins = []
    for i in range(start, end - 1):
        if is_prime(i, mlp) and is_prime(i + 2, mlp):
            twins.append((i, i + 2))
    
    return twins

if __name__ == '__main__':
    # Example usage
    start_range = 1000000
    end_range = 2000000
    
    print(f"Finding twin primes between {start_range} and {end_range}")
    
    # Run and time the calculation
    start_time = time.time()
    twin_primes = find_twin_primes_sequential(start_range, end_range)
    end_time = time.time()
    
    # Print results
    print(f"\nFound {len(twin_primes)} twin prime pairs")
    print(f"Time taken: {end_time - start_time:.2f} seconds")
    
    # Print first few twin primes found (optional)
    if twin_primes:
        print("\nFirst few twin primes found:")
        for pair in twin_primes[:5]:
            print(pair)