.PHONY: all
all: test-core run

.PHONY: run
run:
	python3 main.py

.phony: test
test: test-full

.phony: test-full
test-full:
	python3 -m pylint *.py
	python3 -m flake8 *.py
	python3 -m coverage erase
	python3 -m coverage run -m unittest *_test.py
	python3 -m coverage report -m --fail-under=80

.phony: test-core
test-core:
	python3 -m unittest *_test.py

.phony: reqs
reqs:
	dpkg -V $$(xargs < packages.txt) || sudo apt-get install -y -q $$(xargs < packages.txt)
	pip3 -q install -r requirements.txt
	dpkg -V Leap || sudo dpkg --install LEAP/Leap-2.3.1+31549-x64.deb

.phony: todos
todos:
	grep -n "TODO" *.py|cat -n
