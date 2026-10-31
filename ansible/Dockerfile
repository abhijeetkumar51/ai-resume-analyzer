FROM python:3.13-slim

ENV ANSIBLE_HOST_KEY_CHECKING=False \
    PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir ansible-core docker requests \
    && ansible-galaxy collection install community.docker

WORKDIR /playbooks
COPY playbooks/ /playbooks/

CMD ["sleep", "infinity"]
