feature: .image
	@docker run \
		--env="AWS_ACCESS_KEY=${AWS_ACCESS_KEY}" \
		--env="AWS_SECRET_KEY=${AWS_SECRET_KEY}" \
		--env="AWS_SIMPLEDB_NAME=${AWS_SIMPLEDB_NAME}" \
		metrics /metrics/bin/collect_metrics.py

bootstrap: .image

.image: $(shell find bin) requirements.txt crontab Dockerfile
	docker build --tag metrics .
	touch $@
