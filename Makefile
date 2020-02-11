
.phony: run-tests install-develop

install-develop:
	python3 setup.py develop

run-tests:
	python3 -m unittest discover -s test/
