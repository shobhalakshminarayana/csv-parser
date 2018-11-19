dev:
	docker run -it --rm \
		-v `pwd`:/source \
		-w /source \
		--entrypoint bash \
		python:3
