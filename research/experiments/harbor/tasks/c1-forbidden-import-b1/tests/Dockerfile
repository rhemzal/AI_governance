FROM ubuntu:24.04
RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /tests
COPY check.py /tests/check.py
COPY test.sh /tests/test.sh
COPY expected/ /tests/expected/
RUN chmod 0755 /tests/test.sh
