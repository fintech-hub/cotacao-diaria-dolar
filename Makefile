.PHONY: isort lint test install sh

isort:
	sh -c "isort --skip-glob=.flake8 --recursive . "

lint:
	flake8 .

cov:
	coverage run --source='.' test_dolar.py && coverage report -m

test:
	python ./test_dolar.py

install:
	pipenv install

sh:
	pipenv shell
