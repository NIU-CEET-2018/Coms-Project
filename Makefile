TESTS := $(patsubst %.py,%.test,$(wildcard *.py))

.PHONY: run test
all: run

run:

test: $(TESTS)

reqs:
	pip3 install -r requirements.txt

%.test: %.py
	./$< test
