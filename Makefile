run:
	docker-compose run --rm python-env sh -c '\
	python -m pip install -r requirements.txt && \
	python -m bot.penguin \
		--bot 0 \
		--discord $(DISCORD_TOKEN) \
		--guild "$(GUILD_NAME)" \
		--account $(AWS_ACCOUNT_DSWD)'
.PHONY: run

run-baby:
	docker-compose run --rm python-env sh -c '\
	python -m pip install -r requirements.txt && \
	python -m bot.penguin \
		--bot 1 \
		--discord $(DISCORD_TOKEN) \
		--guild "$(GUILD_NAME)" \
		--account $(AWS_ACCOUNT_DSWD)'
.PHONY: run-baby
