""" lz77 compression algorithm implementation  """

from collections import namedtuple
from typing import List

Triplet = namedtuple("Triplet", ['o', 'l', 'c'])

def get_common_len(s, i, search_buff, j, look_len, wind_len):
    # print(search_buff)
    count = 0
    temp = i
    while i < temp + look_len  and i < len(s) and j < len(search_buff) and s[i] == search_buff[j] and count < wind_len:
        count += 1
        i += 1
        j += 1

    return count


def decompress(decoded_list: List[Triplet]) -> str:
    output = []
    out_len = 0
    for item in decoded_list:
        if item.l == 0:
            output.append(item.c)
            out_len += 1
        else:
            t = output[out_len-item.o:out_len-item.o+item.l]
            output.extend(list(t))
            output.append(item.c)
            out_len += len(t)+1
    
    return "".join(output)


def compress(inputstr: str, wind_len: int, look_ahead_buffer_len: int) -> List[Triplet]:

    n = len(inputstr)
    search_buffer = []
    outputs = []

    i = 0 # for iterating input string
    while i < n:

        search_buff_len = len(search_buffer)
        j = search_buff_len-1 # for iterating the search buffer
        max_len_found = 0 # the maximum length that is found
        found_index = -1 # the starting index where the max length found
        while j >= 0 and search_buff_len - j <= wind_len:
            if inputstr[i] == search_buffer[j]: # if we found a match then check no of matchings at that index
                common_str_len = get_common_len(inputstr, i, search_buffer, j, look_ahead_buffer_len, wind_len)
                if common_str_len > max_len_found:
                    max_len_found = common_str_len
                    found_index = j
                j -= common_str_len
            else:
                j -= 1
        if found_index == -1:
            next_char = ""
            if i + max_len_found < n:
                next_char = inputstr[i+max_len_found]

            output = Triplet(0, 0, next_char)
        else:
            next_char = ""
            if i + max_len_found < n:
                next_char = inputstr[i+max_len_found]

            output = Triplet(i-found_index, max_len_found, next_char)

        outputs.append(output)
        search_buffer.extend(list(inputstr[i:i+max_len_found+1]))

        i += max_len_found + 1

    return outputs


if __name__ == "__main__":
    s1 = "ABABCBCBAABCABe"
    cmp = compress(s1, 4, 4)
    dcmp = decompress(cmp)
    assert s1 == dcmp

    s2 = "abcbbcbaaaaaa"
    cmp = compress(s2, 6, 5)
    dcmp = decompress(cmp)
    assert s2 == dcmp