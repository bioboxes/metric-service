FROM python:2.7
MAINTAINER Michael Barton, mail@michaelbarton.me.uk

RUN apt-get update && \
    apt-get install --yes --no-install-recommends cron

ADD ./requirements.txt /metrics/requirements.txt
RUN pip install -r /metrics/requirements.txt

ADD . /metrics

ADD crontab /etc/cron.d/metrics-cron
RUN chmod 0644 /etc/cron.d/metrics-cron
RUN touch /var/log/cron.log

CMD env | grep -v "TUTUM" > /root/environment && \
    cron && \
    tail -f /var/log/cron.log
