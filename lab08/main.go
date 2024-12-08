package main

import (
	"fmt"
	"math"
	"sync"
	"time"
)

func sumPart(arr []int, start, end int, result *int, wg *sync.WaitGroup, lock *sync.Mutex) {
	localSum := 0
	for i := start; i < end; i++ {
		localSum += arr[i]
	}
	lock.Lock()
	*result += localSum
	lock.Unlock()
	wg.Done()
}

func sumWithTwoThreads(arr []int) int {
	var result int
	var wg sync.WaitGroup
	var lock sync.Mutex

	n := len(arr)
	wg.Add(2)
	go sumPart(arr, 0, n/2, &result, &wg, &lock)
	go sumPart(arr, n/2, n, &result, &wg, &lock)
	wg.Wait()
	return result
}

func sumWithMultipleThreads(arr []int, numThreads int) int {
	var result int
	var wg sync.WaitGroup
	var lock sync.Mutex

	n := len(arr)
	chunkSize := int(math.Ceil(float64(n) / float64(numThreads)))

	for i := 0; i < numThreads; i++ {
		start := i * chunkSize
		end := (i + 1) * chunkSize
		if end > n {
			end = n
		}
		wg.Add(1)
		go sumPart(arr, start, end, &result, &wg, &lock)
	}
	wg.Wait()
	return result
}

func normalSum(arr []int) int {
	sum := 0
	for _, value := range arr {
		sum += value
	}
	return sum
}

func measureTime(name string, f func() int) {
	start := time.Now()
	result := f()
	elapsed := time.Since(start)
	fmt.Printf("%s: Result = %d, Time = %v\n", name, result, elapsed)
}

func main() {
	arr := make([]int, 10000000)
	for i := range arr {
		arr[i] = i + 1
	}

	measureTime("Normal Sum", func() int {
		return normalSum(arr)
	})

	measureTime("Sum with Two Threads", func() int {
		return sumWithTwoThreads(arr)
	})

	measureTime("Sum with Multiple Threads (8)", func() int {
		return sumWithMultipleThreads(arr, 8)
	})
}

