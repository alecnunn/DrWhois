.PHONY: clean

help:
	@echo "clean - move all build and Python artifacts"
	@echo "database - initialize the database with schema"
	@echo "deps - install the dependencies from the requirements.txt dependency list"
	@echo "prepare-deps - generates a new requirements.txt dependency list"

clean:
	rm -rf *.db
	rm -rf *.txt

prepare-deps:
	pip freeze > requirements.txt

deps:
	pip install -r requirements.txt

database:
	sqlite3 drwhois.db < schema.sql