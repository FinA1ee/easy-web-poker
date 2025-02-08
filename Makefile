.PHONY: install test run clean

install:
	pip install -e ".[dev]"

test:
	pytest

run:
	FLASK_APP=src/web_poker/app.py flask run --debug

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete 