up-dep:
	docker-compose up -d
down-dep:
	docker-compose down
run:
	python manage.py runserver
update-pip-dep:
	pip freeze >requirements.txt
build:
	docker build . -t twitter-watch-code --target builder
