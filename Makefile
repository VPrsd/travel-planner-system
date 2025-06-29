# Makefile
.PHONY: install test run clean docker-build docker-run

# Install dependencies
install:
	pip install -r requirements.txt

# Run tests
test:
	python -m pytest test_travel_planner.py -v

# Run with example
run-example:
	python travel_planner.py \
		--destination "Georgia" \
		--budget 1500 \
		--days 7 \
		--travelers 2 \
		--style balanced \
		--preferences culture food hiking wine \
		--output georgia_example.json

# Clean generated files
clean:
	rm -f *.json
	rm -f *.log
	rm -rf __pycache__
	rm -rf .pytest_cache

# Docker commands
docker-build:
	docker build -t travel-planner .

docker-run:
	docker-compose up

# Development setup
dev-setup:
	cp .env.example .env
	echo "Please edit .env with your API keys"
	pip install -r requirements.txt
	pip install pytest pytest-asyncio

# Lint code
lint:
	python -m flake8 travel_planner.py
	python -m black travel_planner.py --check

# Format code
format:
	python -m black travel_planner.py

