docker := docker run \
	  --env="AWS_ACCESS_KEY=${AWS_ACCESS_KEY}" \
	  --env="AWS_SECRET_KEY=${AWS_SECRET_KEY}" \
	  --env="AWS_SIMPLEDB_NAME=${AWS_SIMPLEDB_NAME}" \
	  --env="AWS_S3_BUCKET=${AWS_S3_BUCKET}" \
	  --tty

test := $(docker) metrics /metrics/cron/test

feature: .image
	@$(test) /metrics/bin/collect_metrics.py
	@$(test) /metrics/bin/collate_metrics.py

console: .image
	$(docker) \
		--interactive \
		--rm \
		metrics python -i /metrics/src/console.py

ssh: .image
	$(docker) \
		--interactive \
		--rm \
		metrics /bin/bash

bootstrap: .image

.image: $(shell find bin src cron) requirements.txt Dockerfile
	docker build --tag metrics .
	touch $@
