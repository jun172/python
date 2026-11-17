from typing import List

def comb_sort(numbrs:List[int]) -> List[int]:
    len_numbers = len(numbrs)
    gap = len_numbers
    swapped = True
    
    while gap != 1 or swapped:
        gap = int(gap/1.3)
        if gap < 1:
            gap = 1
        
        swapped = False
        
        for i in range(0,len_numbers - gap):
            if numbrs[i] > numbrs[i + gap]:
                numbrs[i],numbrs[i+gap] = numbrs[i + gap],numbrs[i]
                swapped = True
    return numbrs

if __name__ == "__main__":
    import random
    nums = [random.randint(0,10000) for i in range(100)]
    print(comb_sort(nums))