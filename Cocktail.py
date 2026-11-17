from typing import List


def cocktail_sort(numbers: List[int]) -> List[int]:
    len_numbers = len(numbers)
    swapped = True
    start = 0
    end = len_numbers - 1

    while swapped:
        swapped = False

        # 左から右への走査（最大の要素を右端へ）
        for i in range(start, end):
            if numbers[i] > numbers[i + 1]:
                numbers[i], numbers[i + 1] = numbers[i + 1], numbers[i]
                swapped = True

        # 要素の交換が行われなかった場合はソート完了
        if not swapped:
            break

        swapped = False
        end = end - 1

        # 右から左への走査（最小の要素を左端へ）
        for i in range(end - 1, start - 1, -1):
            if numbers[i] > numbers[i + 1]:
                numbers[i], numbers[i + 1] = numbers[i + 1], numbers[i]
                swapped = True

        start = start + 1

    return numbers


# 動作確認用
if __name__ == "__main__":
    sample_list = [5, 2, 8, 1, 9, 3]
    sorted_list = cocktail_sort(sample_list)
    print("Sorted:", sorted_list)  # Output: [1, 2, 3, 5, 8, 9]