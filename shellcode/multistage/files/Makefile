.PHONY: multistage
FLAG = -O0 -fno-stack-protector -fno-pie -z execstack -no-pie

multistage: multistage.c
    gcc $(FLAG) -o $@ $<

