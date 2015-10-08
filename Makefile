.PHONY: clean

help:
	@echo "clean - move all build and Python artifacts"
	@echo "deps - install the dependencies from the requirements.txt dependency list"
	@echo "prepare-deps - generates a new requirements.txt dependency list"

clean:
	rm -rf scripts/arin.db
	rm -rf requirements.txt

prepare-deps:
	pip freeze > requirements.txt

deps:
	pip install -r requirements.txt
