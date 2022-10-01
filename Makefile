run:
	docker-compose run --rm python-env sh -c '\
	python -m pip install -r requirements.txt && \
	python -m bot.penguin \
		--bot 0 \
		--discord $(DISCORD_TOKEN) \
		--guild "$(GUILD_NAME)"'
.PHONY: run

run-baby:
	docker-compose run --rm python-env sh -c '\
	python -m pip install -r requirements.txt && \
	python -m bot.penguin \
		--bot 1 \
		--discord $(DISCORD_TOKEN) \
		--guild "$(GUILD_NAME)"'
.PHONY: run-baby
