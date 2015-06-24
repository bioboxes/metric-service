bootstrap: .image

.image: $(shell find bin) requirements.txt crontab
	docker build --tag metrics .
	touch $@
