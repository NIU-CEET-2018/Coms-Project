.PHONY: run test
all: run

run:

test:
	python3 -m unittest *_test.py

reqs:
	dpkg -V $$(xargs < packages.txt) 2>&1 | awk '{ print $$3 }'|sed "s/'//g"|xargs -r sudo apt-get install -y -q
	pip3 -q install -r requirements.txt


