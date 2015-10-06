.PHONY: clean

help:
	@echo "clean - move all build and Python artifacts"

clean:
	rm -rf scripts/arin.db

deps:
	pip freeze > requirements.txt


