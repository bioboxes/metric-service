all: .upload

.upload: ./bin/upload_metrics.py data/metrics.yaml
	$^
	touch .upload

data/metrics.yaml: ./bin/fetch_metrics.py
	mkdir -p $(dir $@)
	$^ > $@
