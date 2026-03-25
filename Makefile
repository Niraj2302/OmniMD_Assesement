start:
	docker-compose up --build -d

stop:
	docker-compose down

lint:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	black --check .

test:
	docker-compose exec api pytest --cov=api --cov=agents --cov=rag