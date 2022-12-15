lint:
	black .
	isort .
	mypy .


airflow:
	docker-compose build
	docker build -t predict -f dags/Dockerfile .
	docker-compose up airflow-init
	docker-compose up
