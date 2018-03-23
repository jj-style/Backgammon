def getDig(n,modder,dig_array,maxLength,num):
    dig = n % modder
    actual_dig = int(dig / (modder/10))
    modder *= 10
    new_n = n - dig
    dig_array.append(actual_dig)
    if new_n == 0 and len(dig_array) == maxLength:
        num[2] = dig_array
        return num
    return getDig(new_n,modder,dig_array,maxLength,num)
    
def fillBuckets(n,digits_array,radix_buckets):
    for i in range(len(digits_array)):
        radix_buckets[digits_array[i][2][n]].append(digits_array[i])
    new_digits_array = []
    for bucket in radix_buckets:
        while len(bucket) != 0:
            new_digits_array.append(bucket.pop(0))
    return new_digits_array

def magic(numList):
    sorted_list = []
    for nums in numList:
        s = ''.join(map(str, nums[2][::-1]))
        nums[2] = s
        sorted_list.append(nums)
    return sorted_list

def radix(array):
    radix_buckets = [[] for i in range(10)]
    digits_array = []
    ints_array = []
    for i in array:
        ints_array.append(i[2])
    maxInt = 0
    for i in ints_array:
        if int(i) > maxInt:
            maxInt = int(i)
    maxInt = len(str(maxInt))
    for num in array:
        digits_array.append(getDig(int(num[2]),10,[],maxInt,num))
    for i in range(maxInt):
        digits_array = fillBuckets(i,digits_array,radix_buckets)
    return magic(digits_array)

