def bs(sequence, item):
    begin = 0
    end = len(sequence) - 1
    while begin <= end:
        mid = (begin + end) // 2
        mid_val = sequence[mid]
        if mid_val == item:
            return mid
        elif mid_val > item:
            end = mid - 1
        else:
            begin = mid + 1
    return None
seqA = [2, 4, 6, 7, 8, 9, 10, 12, 34, 45, 52, 66, 70]

itA = 34

print(bs(seqA, itA))