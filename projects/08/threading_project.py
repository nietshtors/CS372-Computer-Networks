import threading

def runner(id, start, end, result):
    result[id] = sum(range(start, end + 1))


ranges = [
    [10, 20],
    [1, 5],
    [70, 80],
    [27, 92],
    [0, 16]
]
THREAD_COUNT = len(ranges)
threads = []
result = [0] * THREAD_COUNT

for i in range(THREAD_COUNT):
    t = threading.Thread(target=runner, args=(i, ranges[i][0], ranges[i][1], result))
    t.start()
    threads.append(t)
    
for t in threads: t.join()
print(result)
print(sum(result))
