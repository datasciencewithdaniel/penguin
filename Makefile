run:
	docker-compose run --rm python-env sh -c '\
	python -m pip install -r requirements.txt && \
	python -m bot.penguin --bot 0'
.PHONY: run

run-baby:
	docker-compose run --rm python-env sh -c '\
	python -m pip install -r requirements.txt && \
	python -m bot.penguin --bot 1'
.PHONY: run-baby