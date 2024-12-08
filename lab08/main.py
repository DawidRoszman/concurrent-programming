import threading
import time
import random
from concurrent.futures import ThreadPoolExecutor

class ListSummarizer:
    def __init__(self, numbers):
        self.numbers = numbers
        self.total_sum = 0
        self.lock = threading.Lock()

    def two_thread_sum(self):
        mid = len(self.numbers) // 2
        
        partial_sums = [0, 0]
        
        def sum_half(start_index, end_index, result_index):
            """Sumuje połowę listy"""
            partial_sum = sum(self.numbers[start_index:end_index])
            partial_sums[result_index] = partial_sum
        
        thread1 = threading.Thread(target=sum_half, 
                                   args=(0, mid, 0))
        
        thread2 = threading.Thread(target=sum_half, 
                                   args=(mid, len(self.numbers), 1))
        
        thread1.start()
        thread2.start()
        
        thread1.join()
        thread2.join()
        
        return sum(partial_sums)

    def multi_thread_sum(self, num_threads=4):
        def worker(thread_numbers):
            return sum(thread_numbers)
        
        chunk_size = len(self.numbers) // num_threads
        chunks = [
            self.numbers[i:i+chunk_size] 
            for i in range(0, len(self.numbers), chunk_size)
        ]
        
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            partial_sums = list(executor.map(worker, chunks))
        
        return sum(partial_sums)

def generate_large_list(size=1_000_000):
    """Generuje dużą listę liczb całkowitych"""
    return [random.randint(1, 100) for _ in range(size)]

def main():
    large_list = generate_large_list(1_000_000_0)
    
    # Standardowe sumowanie (dla porównania)
    start = time.time()
    standard_sum = sum(large_list)
    standard_time = time.time() - start
    print(f"Suma standardowa: {standard_sum}")
    print(f"Czas sumowania standardowego: {standard_time:.4f} s")
    
    # Sumowanie dwuwątkowe
    start = time.time()
    summarizer = ListSummarizer(large_list)
    two_thread_sum = summarizer.two_thread_sum()
    two_thread_time = time.time() - start
    print(f"Suma dwuwątkowa: {two_thread_sum}")
    print(f"Czas sumowania dwuwątkowego: {two_thread_time:.4f} s")
    
    # Sumowanie wielowątkowe
    start = time.time()
    multi_thread_sum = summarizer.multi_thread_sum(num_threads=8)
    multi_thread_time = time.time() - start
    print(f"Suma wielowątkowa: {multi_thread_sum}")
    print(f"Czas sumowania wielowątkowego: {multi_thread_time:.4f} s")

if __name__ == "__main__":
    main()
