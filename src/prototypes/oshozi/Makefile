# -*- mode: makefile-gmake; coding: utf-8 -*-

.ONESHELL:
PRJ = Oshozi

all:

setup:
	@cd $(PRJ)
	./manage.py migrate
	./manage.py makemigrations main
	./manage.py migrate
	./manage.py loaddata  main/data/init_status_data.json

load:
	@cd $(PRJ)
	./manage.py loaddata  main/data/init_status_data.json

superuser:
	@cd $(PRJ)
	./manage.py createsuperuser

run:
	@cd $(PRJ)
	./manage.py runserver 8081

clean:
	$(RM) $(PRJ)/db.sqlite3
	$(RM) -r $(PRJ)/main/migrations/

test:
	@cd $(PRJ)

