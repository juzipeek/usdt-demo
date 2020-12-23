###########################################################
.SUFFIXES: .o .c
.c.o:
	$(CC) -g -c $< -Wall
###########################################################

CC  	= gcc
CFLAGS	=

App		= demo
OBJS	= demo.o

all: $(App) test

.PHONY: deps
deps: probes.h probes.o

$(App) : probes.h $(OBJS) probes.o
	$(CC) -o $@ $?
	@echo -e "\t\t[$@] compile success!"

probes.h: probes.d
	dtrace -C -h -s $< -o $@

probes.o: probes.d $(OBJS)
	dtrace -C -G -s $< -o $@

clear:
	rm -f *.o probes.h $(App)

test:
	stap -L 'process("./demo").mark("*")'