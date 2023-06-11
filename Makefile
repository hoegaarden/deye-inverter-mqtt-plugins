VERSION ?= $(shell git describe --always --dirty)

ARCHS ?= linux/amd64,linux/arm/v7

GH_USER ?= hoegaarden
REPO ?= ghcr.io/$(GH_USER)/deye-inverter-mqtt-plugins
BUILDX_BUILDER ?= deye-inverter-mqtt-plugins
BASE_IMAGE ?= $(REPO):base-$(VERSION)
IMAGE ?= $(REPO):$(VERSION)

test:
	PYTHONPATH="$${PWD}/deye-inverter-mqtt/src" pytest -v plugins

docker.build: test docker.build.base
	docker buildx build \
		--builder "$(BUILDX_BUILDER)" \
		--platform "$(ARCHS)" \
		--build-arg "BASE_IMAGE=$(BASE_IMAGE)" \
		--push \
		--tag "$(IMAGE)" \
		.

docker.build.base: docker.build.setup
	cd deye-inverter-mqtt && docker buildx build \
		--builder "$(BUILDX_BUILDER)" \
		--platform "$(ARCHS)" \
		--push \
		--tag "$(BASE_IMAGE)" \
		.

docker.build.setup:
	docker buildx ls | grep -q "$(BUILDX_BUILDER)" || { \
		docker buildx create --name "$(BUILDX_BUILDER)" ; \
	}

docker.build.cleanup:
	docker buildx ls | grep -q "$(BUILDX_BUILDER)" && { \
		docker buildx rm --builder "$(BUILDX_BUILDER)" ; \
	}
