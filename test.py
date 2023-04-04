import heapq

# Create an empty heap
heap = []

# Add items to the heap with custom priorities
heapq.heappush(heap, (2, 'item2'))
heapq.heappush(heap, (1, 'item1'))
heapq.heappush(heap, (3, 'item3'))

# Get the smallest item from the heap
print(heapq.heappop(heap))
print(heapq.heappop(heap))
