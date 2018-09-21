.PHONY: all
all: test-code run

.PHONY: run
run:
	python3 main.py

.phony: test
test: test-format test-code-and-coverage todos

.phony: test-format
test-format:
	python3 -m pylint *.py
	echo
	python3 -m flake8 *.py
	echo

.phony: test-code-and-coverage
test-code-and-coverage:
	python3 -m coverage erase
	python3 -m coverage run -m unittest *_test.py
	python3 -m coverage report -m --fail-under=80
	echo
	python2 -m coverage erase
	python2 -m coverage run -m unittest *_test2.py
	python2 -m coverage report -m --fail-under=80
	echo

.phony: test-code
test-core:
	python3 -m unittest *_test.py

.phony: reqs
reqs:
	-dpkg -V $$(xargs < packages.txt) 2>&1 |cut -d\' -f2| while read p; do sudo apt-get install -y -q $$p; done
	-sudo python3 -m pip -q install --upgrade -r requirements3.txt
	-sudo python2 -m pip -q install --upgrade -r requirements2.txt
	-dpkg -V Leap || sudo ./Install_Leap_Deamon.sh

.phony: todos
todos:
	grep -n "TODO" *.py | cat -n
