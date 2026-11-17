from typing import List

def gome_sort(numbars: List[int]) -> List[int]:
    len_numbrs = len(numbars)
    index =0
    while index < len_numbrs:
        if index == 0:
            index = index + 1
        if numbars[index] >= numbars[index-1]:
            index = index + 1
        else:
            numbars[index],numbars[index-1] = numbars[index-1],numbars[index]
    return numbars

if __name__ == "__main__":
    import random
    nums =[random.randint(0,1000) for _ in range(10)]
    print(gome_sort(nums))