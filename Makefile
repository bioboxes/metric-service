data/metrics.yaml: ./bin/fetch_metrics.py
	mkdir $(dir $@)
	$^ > $@
