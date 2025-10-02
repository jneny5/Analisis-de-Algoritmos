def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]
        merge_sort(left_half)
        merge_sort(right_half)
        merge(arr, left_half, right_half)
    return arr

def merge(arr, left_half, right_half):
    i = j = k = 0
    while i < len(left_half) and j < len(right_half):
        if left_half[i] < right_half[j]:
            arr[k] = left_half[i]
            i += 1
        else:
            arr[k] = right_half[j]
            j += 1
        k += 1
    while i < len(left_half):
        arr[k] = left_half[i]
        i += 1
        k += 1
    while j < len(right_half):
        arr[k] = right_half[j]
        j += 1
        k += 1

#Merge Sort:
array = [17, 38, 27, 43, 3, 9, 82, 10]
sorted_arr = merge_sort(array)
print("Arreglo ordenado (Merge Sort):", sorted_arr)

print("\n" + "="*50 + "\n")

def quick_sort(arr):
    if len(arr) <= 1:
        return arr  
    pivot = arr[len(arr) // 2] 
    left = [x for x in arr if x < pivot] 
    middle = [x for x in arr if x == pivot] 
    right = [x for x in arr if x > pivot]  
    return quick_sort(left) + middle + quick_sort(right)  
#Quick Sort:
arr = [17, 38, 27, 43, 3, 9, 82, 10]
sorted_arr = quick_sort(arr)
print("Arreglo ordenado (Quick Sort):", sorted_arr)