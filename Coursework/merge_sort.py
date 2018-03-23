def merge(a,b,ob):
    merged = []
    while len(a) != 0 and len(b) != 0:
        if a[0][ob] < b[0][ob] or a[0][ob] == b[0][ob]:
            merged.append(a.pop(0))
        elif a[0][ob] > b[0][ob]:
            merged.append(b.pop(0))
    if len(a) !=0 and len(b) == 0:
        merged += a
    elif len(a) == 0 and len(b) != 0:
        merged += b
    return merged

def mergesort(array,order_by):
    if len(array) == 0 or len(array) == 1:
        return array
    else:
        middle = int(len(array)/2)
        a = mergesort(array[:middle],order_by)
        b = mergesort(array[middle:],order_by)
        return merge(a,b,order_by)
