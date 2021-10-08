from numpy import inner
import numpy as np
import numpy.ma as ma
import math
import logging

"""
brute_search:
Solves a N choose 2 problem with N^2 time complexity using a nested loop 
Also logs # of comparisons

Inputs: 
src_array (an array of integers to be searched through) 
target (the integer two elements of the array should add to)

Output:
num_pairs (the number of pairs found as an integer)
num_comps (the number of comparisons made as an integer)
"""
def brute_search(src_array, target):
    #brute_log = log_setup('brute', 'path', 'w')
    #brute_log.info(f'Beginning brute search. Array is {src_array}, target is {target}')
    num_pairs = 0
    outer_index = 0
    num_comps = 0
    while outer_index < len(src_array):
        inner_index = outer_index + 1 #only compare w/ numbers in "back half"
        while inner_index < len(src_array):
            num_comps += 1
            if src_array[outer_index] + src_array[inner_index] == target:
                num_pairs += 1
            inner_index += 1
        outer_index += 1
    #brute_log.info(f'Ending brute search function. Results: num_pairs -- {num_pairs}, num_comps -- {num_comps})
    return num_pairs, num_comps

"""
binary_search:
Helper function that binary searches an array for a target
Also logs # of comparisons

Inputs: 
src_array (a SORTED array of integers to be searched through) 
target (the integer that needs to be found to create a sum)
begin_index (int representing start of the array region being searched)
end_index (int representing end of the array region being searched)

Output:
num_found (int representing number of targets found found)
num_comps (int representing number of comparisons made)

"""
def binary_search(src_array, target, begin_index, end_index):
    #brute_log = log_setup('binary', 'path', 'w')
    #brute_log.info(f'Beginning binary search. Array is {src_array}, target is {target}')
    num_found, num_comps = 0, 0
    while begin_index <= end_index:
        mid_index = begin_index + math.floor((end_index - begin_index + 1) / 2)
        #binary_logger.info(f'In binary serach. Begin = {begin_index}, End = {end_index}, Mid Index = {mid_index}, Mid Val: {src_array[mid_index]}')
        num_comps += 1
        if src_array[mid_index] == target:
            while mid_index > begin_index and src_array[mid_index - 1] == target:
                mid_index -= 1 #sets mid index to first occurence of target
            while mid_index < len(src_array) - 1 and mid_index >= 0 and src_array[mid_index] == target:
                num_found += 1
                mid_index += 1
            break #there is no more to be done, all are found
        elif begin_index == end_index:
            break
        elif src_array[mid_index] > target:
            end_index = mid_index - 1
        else: #src_array[mid_index] < target
            begin_index = mid_index
        #binary_logger.info(f'Leaving binary search, num found is {num_found}, num comps is {num_comps})
        return num_found, num_comps

"""
sorted_search:
Solves a N choose 2 problem with  time complexity a sort/binary search model
Also logs # of comparisons

Inputs: 
src_array (an array of integers to be searched through) 
target (the integer two elements of the array should add to)

Output:
num_pairs (the number of pairs found as an integer)
num_comps (the number of comparisons made as an integer)
"""
def sorted_search(src_array, target):
    #sorted_logger = log_setup('sorted', 'C:\\Users\\eshner\\OneDrive\\Gonzaga\\code\\logs\\sorted.log', 'w')
    working_array = np.sort(src_array)
    #sorted_logger.info(f'inside sorted search, sorted array is: {working_array}, target is {target}')   
    num_pairs = 0
    num_comps = 0
    array_size = len(working_array)
    for cur_index in range(0, array_size):
        cur_num = working_array[cur_index]
        #sorted_logger.info(f'inside sorted pairs func, src array is {working_array} target is {target} num is {cur_num}, searching for {target - cur_num}, num_pairs is {num_pairs}')
        binary_res, search_comps = binary_search(working_array, target - cur_num, cur_index + 1, array_size - 1)
        #sorted_logger.info(f'inside sorted pairs, search result is {binary_res} and number of comps is {num_comps}')
        num_pairs += binary_res
        num_comps += search_comps
    #sorted_logger.info(f'Leaving sorted search, num pairs is {num_pairs}, num comps is {num_comps}')   
    return num_pairs, num_comps

"""
pointers_search:
Solves a N choose 2 problem with   time complexity using a 
Also logs # of comparisons

Inputs: 
src_array (an array of integers to be searched through) 
target (the integer two elements of the array should add to)

Output:
num_pairs (the number of pairs found as an integer)
num_comps (the number of comparisons made as an integer)
"""
def pointers_search(src_array, target):
    #pointers_logger = log_setup('pointers', 'path', 'w')
    working_array = np.sort(src_array) #uses a library to sort array
    #pointers_logger.info(f'Beginning binary search. Sorted array is {working_array}, target is {target}')
    num_pairs, num_comps, beg_ptr = 0, 0, 0
    end_ptr = len(working_array) - 1
    while beg_ptr < end_ptr:
        sum = working_array[beg_ptr] + working_array[end_ptr]
        num_comps += 1
        #if more or less, increment low/high number up/down. 
        if sum < target:
            beg_ptr += 1
        elif sum > target:
            end_ptr -= 1
        else: #if found
            beg_dups = 1
            end_dups = 1
            #then, find all duplicates on both ends
            while beg_ptr < end_ptr - 1 and working_array[beg_ptr + 1] == working_array[beg_ptr]:
                beg_ptr += 1
                beg_dups += 1
            while end_ptr > beg_ptr + 1 and working_array[end_ptr - 1] == working_array[end_ptr]:
                end_ptr -= 1
                end_dups += 1
            num_pairs += beg_dups * end_dups
            num_comps += beg_dups + end_dups
            #increment and keep going
            beg_ptr += 1
            end_ptr -= 1
    #pointers_logger.info(f'Leaving pointers search, num pairs is {num_pairs}, num comps is {num_comps}')
    return num_pairs, num_comps
