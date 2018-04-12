TESTS := $(patsubst %.py,%.test,$(wildcard *.py))

.PHONY: run test
all: run

run:

test: $(TESTS)

%.test: %.py
	./$< test
