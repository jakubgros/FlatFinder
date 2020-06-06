def find_slice(a_list, the_slice):

    slice_len = len(the_slice)
    for i in range(len(a_list)):
        if a_list[i:i+slice_len] == the_slice:
            return i
    return None
