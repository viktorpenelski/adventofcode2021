from typing import List


def count_increasing(data: List[int]) -> int:
    increases = 0
    for i in range(1, len(data)):
        if data[i] > data[i - 1]:
            increases += 1
    return increases


def sliding_windows_3_from(data: List[int]) -> List[int]:
    return [data[i-2] + data[i-1] + data[i] for i in range(2, len(data))]


with open('in.txt') as f:
    values = list(map(int, f.readlines()))

print(count_increasing(values))
print(count_increasing(sliding_windows_3_from(values)))
