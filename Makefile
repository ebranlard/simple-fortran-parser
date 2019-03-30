.PHONY: test

all:
	python test/test_parse.py

test:
	python -m unittest discover
	make -C test

install:
	python -m pip install -e .

dep:
	python -m pip install -r requirements.txt

