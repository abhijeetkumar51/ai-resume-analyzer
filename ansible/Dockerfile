FROM python:3.13-slim

ENV ANSIBLE_HOST_KEY_CHECKING=False \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends docker.io \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir ansible-core docker \
    && ansible-galaxy collection install community.docker

WORKDIR /playbooks
COPY playbooks/ /playbooks/

CMD ["sleep", "infinity"]
