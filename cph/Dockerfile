# Pull base image
FROM python:3.7
# Set environment varibles
WORKDIR /code/
# Install dependencies
RUN pip install pipenv
COPY Pipfile /code/
RUN pipenv lock
RUN pipenv install --system --dev
COPY fetchwaitingtime.py /code/fetchwaitingtime.py
RUN apt-get update && apt-get -y install cron nano
COPY crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab
CMD ["cron", "-f"]
