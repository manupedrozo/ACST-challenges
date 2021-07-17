from pwn import *

'''
The code is unpacked in the main, debug with gdb and do: disassemble 0x400f58,+300 right before the int3 interrupt.
At 0x400f58 we have the signal handler.
See commented assembly below.
    - key1 and magic can be obtained from ghidra once we know their addressess from the assembly
'''

key1 = [0xE8, 0x3A ,0x63 ,0x97 ,0x62 ,0x5E ,0x8C ,0x39 ,0xA2 ,0xB7 ,0x5F ,0xF0 ,0x11 ,0x80 ,0xED ,0x77 ,0x05 ,0x66 ,0x5D ,0xC4 ,0x81 ,0xFF ,0x3C ,0x0E ,0xB5 ,0xB2 ,0x2B ,0xA4 ,0xC8 ,0x9E ,0xCC ,0xC7 ,0x17 ,0x21 ,0x3B ,0x62 ,0x2E ,0x26 ,0x9B ,0xEC]

magic = [0x8e ,0x56 ,0x02 ,0xf0 ,0x19 ,0x6a ,0xe2 ,0x4d ,0x93 ,0xe8 ,0x2d ,0xc3 ,0x67 ,0xdf ,0x80 ,0x43 ,0x76 ,0x12 ,0x6e ,0xb6 ,0xb4 ,0xa0 ,0x58 ,0x3d ,0x85 ,0xd0 ,0x4d ,0xd1 ,0xbb ,0xfd ,0xf8 ,0xb3 ,0x24 ,0x7e ,0x08 ,0x18 ,0x1f ,0x4a ,0xe2 ,0x91 ,0x00]

flag = ""
for i in range(len(magic)-1):
    flag += chr(key1[i] ^ magic[i])


print(f"Flag: {flag}")
#flag{4nt1_r3v_m4st3r5_d30bfusc4t3_3z1ly}

'''
----- signal handler -----

Variables:
- [rbp-0x20]: 0x7fffffffdfc9 -> input string
- [rbp-0x28]: 0x400f28 -> key1
- [rbp-0x30]: 0x401048 -> magic
- [rbp-0x4] : index in flag_string
- [rbp-0x8] : bool flag correct



push   rbp
mov    rbp,rsp
movabs rsi,0x7fffffffdfc9
movabs rdx,0x400f28
movabs rcx,0x401048
mov    DWORD PTR [rbp-0x14],edi
mov    QWORD PTR [rbp-0x20],rsi
mov    QWORD PTR [rbp-0x28],rdx
mov    QWORD PTR [rbp-0x30],rcx
mov    DWORD PTR [rbp-0x8],0x1
mov    DWORD PTR [rbp-0x4],0x0
jmp    0x400fda                     # jump to jmp_1

jump_2:
mov    eax,DWORD PTR [rbp-0x4]
movsxd rdx,eax
mov    rax,QWORD PTR [rbp-0x20]
add    rax,rdx
movzx  ecx,BYTE PTR [rax]
mov    eax,DWORD PTR [rbp-0x4]
movsxd rdx,eax
mov    rax,QWORD PTR [rbp-0x28]
add    rax,rdx
movzx  eax,BYTE PTR [rax]
xor    ecx,eax                      # flag[index] ^ key1[index]
mov    eax,DWORD PTR [rbp-0x4]
movsxd rdx,eax
mov    rax,QWORD PTR [rbp-0x30]
add    rax,rdx
movzx  eax,BYTE PTR [rax]
cmp    cl,al                        # flag[index] ^ key1[index] == magic[index]
je     0x400fd6                     # jump to jmp_3 if correct
mov    DWORD PTR [rbp-0x8],0x0      # set bool to 0 if not correct

jump_3:
add    DWORD PTR [rbp-0x4],0x1      # increment index

jump_1:                             # while for each flag char
mov    eax,DWORD PTR [rbp-0x4]
movsxd rdx,eax
mov    rax,QWORD PTR [rbp-0x28]
add    rax,rdx
movzx  eax,BYTE PTR [rax]
test   al,al
jne    0x400f99                     # jump to jmp_2 (while loop through flag string)

cmp    DWORD PTR [rbp-0x8],0x1
jne    0x401044                     # jump to jump_4
push   0xa
push   0x21656e6f
push   0x20746867
push   0x69722065
push   0x68742074
push   0x6f672065
push   0x7627756f
push   0x79202c74
push   0x61657247
mov    rdi,0x1
mov    rsi,rsp
mov    rdx,0x42
mov    rax,0x1
syscall
xor    rdi,rdi
mov    rax,0x3c
syscall

jump_4:
nop
pop    rbp
ret
'''
