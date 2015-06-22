FROM python:2.7
MAINTAINER Michael Barton, mail@michaelbarton.me.uk

ADD . /metrics
WORKDIR metrics

RUN pip install -r requirements.txt

CMD ['make']
