from typing import List
import random

def merge_sort(numbers: List[int]) -> List[int]:
    if len(numbers) <= 1:
        return numbers
    
    center = len(numbers) // 2
    # 左右それぞれを再帰的にソート
    left = merge_sort(numbers[:center])
    right = merge_sort(numbers[center:])
    
    i = j = k = 0
    # 左右を比較して結合
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            numbers[k] = left[i]
            i += 1
        else:
            numbers[k] = right[j]
            j += 1
        k += 1 
        
    # 残った要素を埋める
    while i < len(left):
        numbers[k] = left[i]
        i += 1
        k += 1
        
    while j < len(right):
        numbers[k] = right[j]
        j += 1
        k += 1
        
    return numbers

if __name__ == "__main__":
    # 0から100までのランダムな整数を100個生成
    nums = [random.randint(0, 100) for _ in range(100)]
    
    print("--- ソート前 ---")
    print(nums)
    
    # マージソートを実行
    sorted_nums = merge_sort(nums)
    
    print("\n--- ソート後 ---")
    print(sorted_nums)