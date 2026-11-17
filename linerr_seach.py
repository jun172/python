from typing import List, NewType

IndexNum = NewType('IndexNum', int)

def linear_search(numbers: List[int], value: int) -> IndexNum:
    for i in range(len(numbers)):
        if numbers[i] == value:
            return IndexNum(i)
    return IndexNum(-1)

def binary_search(numbers: List[int], value: int) -> IndexNum:
    left, right = 0, len(numbers) - 1 
    while left <= right:  # 修正: '<-' から '<=' に修正
        mid = (left + right) // 2
        if numbers[mid] == value:
            return IndexNum(mid)
        elif numbers[mid] < value:
            left = mid + 1
        else:
            right = mid - 1  # 追加: 値が小さい場合の処理
    return IndexNum(-1)      # 追加: 見つからなかった場合

if __name__ == "__main__":
    import random 
    # 二分探索を行うためには、リストが昇順にソートされている必要があります
    nums = sorted([random.randint(0, 100) for _ in range(20)])
    print("ソート済みのリスト:", nums)
    
    # テストとしてリスト内の適当な値を検索
    target = nums[5]
    print(f"線形探索 ({target}):", linear_search(nums, target))
    print(f"二分探索 ({target}):", binary_search(nums, target))
