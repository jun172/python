from typing import List


def insertion_sort(arr: List[int]) -> List[int]:
    """バケット内で使う挿入ソート"""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def bucket_sort(numbers: List[int]) -> List[int]:
    if not numbers:
        return numbers

    # 0割を防ぐため、最大値が0の場合の考慮と、範囲の安全化
    max_num = max(numbers)
    len_numbers = len(numbers)

    # バケットの数をリストの長さと同じにする
    buckets = [[] for _ in range(len_numbers)]

    # 各要素を適切なバケットに振り分ける
    # (max_num + 1 を使うことで、最大値がインデックスを超えないようにする)
    for num in numbers:
        index = (num * len_numbers) // (max_num + 1)
        buckets[index].append(num)

    # 各バケットの中をソートして結果をまとめる
    result = []
    for bucket in buckets:
        insertion_sort(bucket)
        result.extend(bucket)

    return result


if __name__ == "__main__":
    import random

    nums = [random.randint(0, 100) for _ in range(10)]
    print("実行前:", nums)
    print("実行後:", bucket_sort(nums))
