lint:
	black .
	isort .

airflow:
	docker-compose build
	docker build -t train_predict -f dags/Dockerfile .
	docker-compose up airflow-init
	docker-compose up

run-tests:
	docker build -t tests -f Dockerfile_tests .
	docker run tests