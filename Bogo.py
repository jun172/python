import random
from typing import List

def bogo_sort(numbers:List[int]) -> List[int]:
    while not in_order(numbers):
        random.shuffle(numbers)
    return numbers

def in_order(numbers:list) -> bool:
    return all(numbers[i] <= numbers[i +1] for i in range(len(numbers)-1))

if __name__ == "__main__":
    # 要素数を小さく（例: 5個）にする
    nums = [random.randint(0, 100000) for _ in range(100)]
    print("ソート前:", nums)
    print("ソート後:", bogo_sort(nums))