from typing import List

def counting_sort(numbers: List[int], place: int) -> List[int]:
    if not numbers:
        return numbers

    # 桁ごとの数字は 0〜9 なので、サイズは常に 10 でOK
    counts = [0] * 10
    result = [0] * len(numbers)

    # 1. 指定した桁（place）の数字の出現回数を数える
    for num in numbers:
        digit = (num // place) % 10
        counts[digit] += 1

    # 2. 累積和を計算する
    for i in range(1, len(counts)):
        counts[i] += counts[i - 1]

    # 3. 後ろから前に向かって走査し、resultに並べる（安定ソートにするため）
    i = len(numbers) - 1
    while i >= 0:
        num = numbers[i]
        digit = (num // place) % 10
        result[counts[digit] - 1] = num  # 正しい位置に格納
        counts[digit] -= 1  # 同じ数字があるときのためにカウントを減らす
        i -= 1

    return result


def radix_sort(numbers: List[int]) -> List[int]:
    if not numbers:
        return numbers

    max_num = max(numbers)
    place = 1
    
    # 桁をシフトしていき、すべての桁を処理し終わるまでループする
    while max_num // place > 0:
        numbers = counting_sort(numbers, place)
        place *= 10
        
    return numbers


if __name__ == "__main__":
    import random

    nums = [random.randint(0, 10000) for _ in range(100)]
    print("ソート結果:", radix_sort(nums))