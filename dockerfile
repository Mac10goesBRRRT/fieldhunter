FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
      python3.8 python3.8-venv python3.8-dev python3-pip \
      tshark libpcap-dev build-essential git \
    && rm -rf /var/lib/apt/lists/*

RUN python3.8 -m venv /venv && /venv/bin/pip install -U pip setuptools wheel
WORKDIR /app

# Abhängigkeiten zuerst (Layer-Cache)
COPY requirements.txt /tmp/req-fh.txt
COPY sub/nemere/requirements.txt /tmp/req-nemere.txt
RUN grep -vi '^pcapy' /tmp/req-nemere.txt > /tmp/req-nemere-clean.txt \
 && /venv/bin/pip install -r /tmp/req-fh.txt -r /tmp/req-nemere-clean.txt \
      pcapy-ng tabulate ipython

ENV PYTHONPATH=/app/src:/app/sub/nemere/src
ENV PATH=/venv/bin:$PATH
#handle spd-say
RUN printf '#!/bin/sh\necho "$@"\n' > /usr/local/bin/spd-say \
 && chmod +x /usr/local/bin/spd-say
CMD ["bash"]
