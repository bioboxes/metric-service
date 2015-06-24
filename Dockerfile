FROM python:2.7
MAINTAINER Michael Barton, mail@michaelbarton.me.uk

RUN apt-get update && \
    apt-get install --yes --no-install-recommends cron

ADD ./requirements.txt /metrics/requirements.txt
RUN pip install -r /metrics/requirements.txt

ADD . /metrics
