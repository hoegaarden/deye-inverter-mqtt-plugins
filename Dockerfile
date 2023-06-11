ARG BASE_IMAGE
FROM "${BASE_IMAGE}"

ARG PLUGINS_DIR=./plugins
ARG USER=nobody
ARG GROUP=nobody

COPY plugins/stdout-publisher/deye_plugin_stdout_publisher.py "${PLUGINS_DIR}/"

RUN chown -R "${USER}:${GROUP}" .
USER "${USER}"

ENV LOG_STREAM=STDERR
ENV PLUGINS_DIR="${PLUGINS_DIR}"
