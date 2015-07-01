feature: .image
	@docker run \
		--env="AWS_ACCESS_KEY=${AWS_ACCESS_KEY}" \
		--env="AWS_SECRET_KEY=${AWS_SECRET_KEY}" \
		--env="AWS_SIMPLEDB_NAME=${AWS_SIMPLEDB_NAME}" \
		--tty \
		metrics \
		/metrics/cron/test /metrics/bin/collect_metrics.py

console: .image
	@docker run \
		--env="AWS_ACCESS_KEY=${AWS_ACCESS_KEY}" \
		--env="AWS_SECRET_KEY=${AWS_SECRET_KEY}" \
		--env="AWS_SIMPLEDB_NAME=${AWS_SIMPLEDB_NAME}" \
		--interactive \
		--tty \
		--rm \
		metrics python -i /metrics/src/console.py

bootstrap: .image

.image: $(shell find bin src cron) requirements.txt Dockerfile
	docker build --tag metrics .
	touch $@
