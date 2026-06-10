.PHONY: install run test lint format clean

install:
	pip install -e .
	pip install -r requirements-dev.txt

run:
	python -m aigen_html

test:
	pytest -v

lint:
	ruff check src/ tests/

format:
	ruff format src/ tests/

clean:
	rm -rf *.egg-info dist build .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
