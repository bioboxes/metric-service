feature: .image
	@docker run \
		--env="AWS_ACCESS_KEY=${AWS_ACCESS_KEY}" \
		--env="AWS_SECRET_KEY=${AWS_SECRET_KEY}" \
		--env="AWS_SIMPLEDB_NAME=${AWS_SIMPLEDB_NAME}" \
		metrics /metrics/process_metrics

bootstrap: .image

.image: $(shell find bin src) requirements.txt crontab process_metrics
	docker build --tag metrics .
	touch $@
